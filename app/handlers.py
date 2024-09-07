from starlette.exceptions import HTTPException as StarletteHTTPException

from app import app
from .shortcuts import render, redirect
from .exceptions import LoginRequiredException


@app.exception_handler(StarletteHTTPException)
async def http_exception(request, exception):
    '''
        Generic exception handler method for our backend
        StarletteHTTPException most probably won't handle http 500 internal server error
    '''
    status_code = exception.status_code
    template_name = 'errors/main.html'
    context = {
        "status_code": status_code,
        "msg": exception.detail}
    return render(request, template_name, context, status_code)


@app.exception_handler(LoginRequiredException)
async def login_required_exception_handler(request, exception):
    '''custom exception handler for log in'''
    path = request.url.path
    return redirect(request, f'/login?next={path}', remove_session=True)
