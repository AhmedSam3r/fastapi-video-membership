from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import uuid
from app.config import get_settings

from . import validators, security

from app import exceptions

settings = get_settings()


class User(Model):
    # keyspace could be testing or production so we need it to be flexible in case of automated test based on the keyspace name
    __keyspace__ = settings.astradb_keyspace
    email = columns.Text(primary_key=True)
    # we don't want to call the function itself in default, we want to pass 
    # it as callable (now i get it in sqlalchemy flask)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()
    #email_verified = columns.Boolean()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"

    @staticmethod
    def create_user(email, password=None):
        '''
        similar to User.objects.create() but we perform our own validations/checks
        similar to django orm
        '''
        q = User.objects.filter(email=email)
        if q.count() != 0:
            raise exceptions.UserHasAccountException("Email already exists")
        valid, msg, email = validators._validate_email(email)
        if valid is False:
            raise exceptions.InvalidEmailException(msg)

        obj = User(email=email)
        obj.set_password(password)
        obj.save()
        return obj


    def set_password(self, pw, commit=False):
        pw_hash = security.generate_hash(pw)
        self.password = pw_hash
        if commit:
            self.save()

        return True

    def verify_password(self, pw_raw):
        '''
        hashed password is like this
            ===> '$argon2id$v=19$m=65536,t=3,p=4$2CPaAPkykCT6sHzFBesqdg$87TGBOHS7p+34qMyYR7z32NhOQiumA5C6sjGLm4SLW8'
        '''
        pw_hash = self.password
        verified, msg = security.verify_password(pw_hash, pw_raw)
        return verified

    @staticmethod
    def get_user_by_id(user_id=None):
        if user_id is None:
            return None

        q = User.objects(user_id=user_id).allow_filtering()
        if q.count() != 1:
            return None

        return q.first()


'''
in the shell type python
notice here the ISSUE that the shell allowed two users with the same email and the passwords are saved in plain text
>>> from app.users.models import User
>>> User.objects.create(email='ahmed.organising@gmail.com', password='admin')
# get an error here since we haven't initialized the session
>>> from app import db
>>> DB_SESSION = db.get_session() # no need to sync the table 
>>> User.objects.create(email='ahmed.organising@gmail.com', password='admin')
User(email=ahmed.organising@gmail.com, user_id=d2489fca-709c-11ee-b051-e91f02349b61)
>>> User.objects.create(email='ahmed.organising@gmail.com', password='admin2')
User(email=ahmed.organising@gmail.com, user_id=1c82e92e-709d-11ee-b051-e91f02349b61)
>>> user.password
'$argon2id$v=19$m=65536,t=3,p=4$2CPaAPkykCT6sHzFBesqdg$87TGBOHS7p+34qMyYR7z32NhOQiumA5C6sjGLm4SLW8'
'''
