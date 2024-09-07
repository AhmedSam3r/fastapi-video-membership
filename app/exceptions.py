from fastapi import HTTPException


class LoginRequiredException(HTTPException):
    pass


class GenericException(HTTPException):
    pass


class UserHasAccountException(Exception):
    """Custom User already has an account Exception"""


class InvalidEmailException(Exception):
    """Custom invalid email Exception"""


class InvalidUserException(Exception):
    """Custom invalid email Exception"""

class InvalidVideoURLException(Exception):
    """Custom invalid email Exception"""

class VideoAlreadyAddedException(Exception):
    """Custom invalid email Exception"""
