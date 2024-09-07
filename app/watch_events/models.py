import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app import config

settings = config.get_settings()


class WatchEvent(Model):
    __keyspace__ = settings.astradb_keyspace

    event_id = columns.TimeUUID(primary_key=True,
                                default=uuid.uuid1,
                                # clustering_order="DESC" it's not working, why ? what's partition and 
                                # https://stackoverflow.com/questions/41304051/cassandra-abstract-model-cant-define-primary-key-with-clustering-order
                                )
    host_id = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True)
    path = columns.Text()
    start_time = columns.Double()
    end_time = columns.Double()
    duration = columns.Double()
    complete = columns.Boolean(default=False)

    @property
    def is_completed(self):
        return (self.duration * 0.97) < self.end_time

    @staticmethod
    def get_resume_time(host_id, user_id):
        resume_time = 0
        obj = WatchEvent.objects(host_id=host_id, user_id=user_id).\
            allow_filtering().first()
        if obj:
            # if obj.complete is False: #removed it for now no need it for it now             
            resume_time = obj.end_time

        return resume_time

    def __str__(self):
        return f"user_id::{str(self.user_id)[0:8]}--host_id::{self.host_id}--start_time={self.start_time} &&end_time={self.end_time}"
