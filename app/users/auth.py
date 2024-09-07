from .models import User
from jose import jwt, exceptions
import datetime
from app.config import get_settings

settings = get_settings()


def authenticate(email, password):
    '''
    get works with primary key as email is our PK
    to work with non-indexed PK in datastax and cassaandra use it in this format:
        User.objects(user_id='1c82e92e-709d-11ee-b051-e91f02349b61').allow_filtering()
    Note that In this example, you create a SQLAlchemy engine for Cassandra, create a session, and then execute a raw CQL query that includes ALLOW FILTERING. The result is processed in the loop, and the session is closed when you're done.
    Keep in mind that using raw CQL queries with allow_filtering should be done with caution, as it may not be efficient for large datasets. Be aware of potential performance implications, especially if you are working with a significant amount of data. Consider optimizing your Cassandra data model, using secondary indexes where appropriate, and carefully evaluating the use of allow_filtering in your queries.
    cassandra.cqlengine.query.QueryException: Filtering on a clustering key without a partition key is not allowed unless allow_filtering() is called on the queryset. You might want to consider setting custom_index on fields that you manage index outside cqlengine.
    '''
    user: User = User.objects.get(email=email)
    print("user = ", user)
    print("verify pw ", user.verify_password(password))
    if not user or not user.verify_password(password):
        return None

    return user


def login(user, expires_after_sec=settings.session_duration_sec):
    print("session_duration_sec = ", expires_after_sec)
    raw_data = {
        "user_id": f"{user.user_id}",
        "role": "admin",
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_after_sec)
    }
    return jwt.encode(raw_data, settings.secret_key, algorithm=settings.jwt_algorithm)   


def verify_token(token):
    data = None
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except exceptions.ExpiredSignatureError as e:
        data = None
    except Exception:
        pass

    if not data or 'user_id' not in data:
        return None

    return data
