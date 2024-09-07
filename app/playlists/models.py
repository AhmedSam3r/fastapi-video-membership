from datetime import datetime
import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app import config
settings = config.get_settings()

class Playlist(Model):
    __keyspace__ = settings.astradb_keyspace

    db_id = columns.UUID(primary_key=True,
                         default=uuid.uuid1)
    user_id = columns.UUID()
    created_at = columns.DateTime(default=datetime.now)
    updated_at = columns.DateTime()
    hosts_ids = columns.List(value_type=columns.Text)  # we want list of strings 
    title = columns.Text()

    def save(self):
        '''overriding the original method to customize updated_at'''
        # Update updated_at before saving
        self.updated_at = datetime.now()
        super(Playlist, self).save()



