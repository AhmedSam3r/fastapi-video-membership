from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials,
)
from .users import auth
from .users.models import User


class CustomSimpleUser(SimpleUser):
    '''
    inheriting the SimpleUser to add custom attributes such as email
    we can tweak the class more since the session_id token only contains user id for security concerns
    '''
    email: str = None

    def __init__(self, user: dict) -> None:
        user_id: str = user.get('user_id')
        user: User = User.objects(user_id=user_id).allow_filtering().first()
        self.email = user.email
        # calling the parent SimpleUser class method  (username)  
        super().__init__(user_id)


class JWTCookieBackend(AuthenticationBackend):
    '''
    in the backend you must return the auth credentials and the user classes 
        from the starlette.authentication 
        else it gives an error:
            scope["auth"], scope["user"] = auth_result
            TypeError: cannot unpack non-iterable AuthCredentials object
    '''

    async def authenticate(self, request):
        session_token = request.cookies.get("session_id")
        user = auth.verify_token(session_token) if session_token else None
        if user is None:
            roles = ["anon"]
            return AuthCredentials(roles), UnauthenticatedUser()

        roles = ['authenticated']
        return AuthCredentials(roles), CustomSimpleUser(user)
