from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse


from functools import wraps

from .users.auth import verify_token
from .exceptions import LoginRequiredException


def login_required_older(func):

    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        session_token = request.cookies.get('session_id')
        if session_token is None:
            raise HTTPException(status_code=400, detail='wrapper method Not logged in, No session id')  # noqa: E501

        user_session = verify_token(session_token)
        if user_session is None:
            raise LoginRequiredException(status_code=400)


        result = await func(request, *args, **kwargs)

        if isinstance(result, HTMLResponse):
            # Handle HTMLResponse differently
            # You can modify or check the HTML response here
            # For example, adding some custom content
            content = f"<p>Custom message for HTMLResponse: {result.content}</p>"
            result.content = content
            return result

        return result


    return wrapper


'''
after adding the backend and the authentication middle ware in our class
we can refactor the login_required method
since they almost do the same thing
'''


def login_required(func):

    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if request.user.is_authenticated is False:
            print("WORKING LOGIN REQUIRED")
            raise LoginRequiredException(status_code=401)

        return await func(request, *args, **kwargs)

    return wrapper
