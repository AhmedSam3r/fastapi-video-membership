from pydantic import (
    BaseModel,
    validator,
    model_serializer,
    field_validator,
    ValidationInfo
)

from .extractors import extract_video_id
from .models import Video   
from app.exceptions import GenericException, InvalidVideoURLException, VideoAlreadyAddedException



class VideoCreateSchema(BaseModel):
    url: str
    user_id: str
    title: str

    @field_validator("url")
    def validate_youtube_url(cls, field: str, info: ValidationInfo):
        url = field
        video_id = extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} invalid youtube id ")

        return url

    @model_serializer(mode="plain")
    def validate_video(self, value, **kawrgs):
        '''the exceptions here in schemas is user-facing exceptions so we must handle it
            for the user to see proper error messages
            errors in the add_video are system-exceptions if we can call it so
            we catch the exceptions coming from the Video Model and raise value error on own
            SELF.__dict__ =  {'url': 'https://www.youtube.com/watch?v=KQ-u4RcFLBY', 'user_id': 'a820381e-73be-11ee-b051-e91f02349b61'}
        '''
        print("@@@@@@@@@@@validate_video@@@@@@@@@@@@")
        url = self.url
        if url is None:
            raise ValueError(f"provide url is requrired")
        user_id = self.user_id
        video = None
        try:
            video = Video.add_video(url, user_id, title=self.title)
            print("VIDEO IS ", video, video.title)
        except InvalidVideoURLException:
            raise ValueError(f'{url} Invalid YT video url')
        except VideoAlreadyAddedException:
            raise ValueError(f'{url} Video Already Added')

        if not isinstance(video, Video):
            raise ValueError('Problem with saving video')

        return video.get_raw_data() # returns {}
