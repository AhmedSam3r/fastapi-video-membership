from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import uuid
import datetime

from app.exceptions import GenericException, InvalidUserException, VideoAlreadyAddedException, InvalidVideoURLException
from app.config import get_settings
from app.users.models import User

from .extractors import extract_video_id


settings = get_settings()


class Video(Model):
    __keyspace__ = settings.astradb_keyspace
    host_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    host_service = columns.Text(default='youtube')
    url = columns.Text()
    user_id = columns.UUID()
    # newly added title field which needed no migration and we didn't stop the db to take effect
    title = columns.Text()
    created_at = columns.DateTime(default=datetime.datetime.now())
    
    def __str__(self):
        '''must always return string only'''
        return self.__repr__()

    def __repr__(self):
        return f"Video(title={self.title}, host_id={self.host_id}, user_id={self.user_id})"

    @staticmethod
    def add_video(url, user_id, **kawrgs):
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidVideoURLException('Invalid Youtube video URl')
        user: User = User.get_user_by_id(user_id) if user_id else None
        if user.user_id is None:
            raise InvalidUserException('Invalid UserId for Youtube video')
        count = Video.objects(host_id=host_id, user_id=user.user_id).allow_filtering().count()
        if count != 0:
            raise VideoAlreadyAddedException('Video Already Added')

        return Video.create(host_id=host_id, url=url, user_id=user.user_id, **kawrgs)

    def get_raw_data(self):
        return {f"title: {self.title}, host_service:{self.host_service}": self.host_id, "path": self.path}

    @property
    def path(self):
        return f"/videos/{self.host_id}"
    
    def render(self):
        basename = self.host_service # youtube, vimeo ... etc.
        template_name = f"/videos/renderers/{basename}.html"
        print("TEMPLATE NAME = ", template_name)
        context = {"host_id": self.host_id}
        t = settings.templates.get_template(template_name)
        return t.render(context)
