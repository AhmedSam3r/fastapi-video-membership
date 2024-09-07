import pytest

from app.users.models import User
from app import db


@pytest.fixture(scope='module')
def setup():
    # setup part
    session = db.get_session()
    yield session
    # teardown part
    q = User.objects.filter(email='test@test.com')
    if q.count != 0:
        print("WE ARE DELETING")
        q.delete()
    session.shutdown()


def test_create_user(setup):
    '''
    I got this error
    app/test_users.py:3: in <module>
    from app.users.models import User
    ModuleNotFoundError: No module named 'app'
    when I ran pytest .
    to solve it:
    ADD __init__.py in the app directory to resolve the relative import
    '''

    User.create_user(email='test@test.com', password='abc123')


def test_duplicate_user(setup):
    # Exception is too generic as the project progress,
    # each exception should have a name or type UserDoesnotExist ...etc.
    with pytest.raises(Exception):
        User.create_user(email='test@test.com', password='abc123')


def test_invalid_email():
    with pytest.raises(Exception):
        User.create_user(email='test1@test', password='abc123')


def test_valid_password(setup):
    q = User.objects.filter(email='test@test.com')
    assert q.count() == 1
    user_obj = q.first()
    assert user_obj.verify_password('abc123') is True
    assert user_obj.verify_password('abc') is False


def test_assert():
    assert True is True


def test_invalid_assert():
    with pytest.raises(AssertionError):
        assert True is False
