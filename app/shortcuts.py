'''similar to the django render, redirect method
    coming from django background, you're inspired by the way django works
rendering html template based on the request'''

from app.config import get_settings
from fastapi import Request, responses
from app.exceptions import GenericException
from cassandra.cqlengine.query import DoesNotExist, MultipleObjectsReturned

settings = get_settings()
BASE_DIR = settings.base_dir
templates = settings.templates



def render(request: Request, template_name: str, context: dict = {},
           status_code=200, cookies: dict = {}) -> responses.HTMLResponse:

    ctx = context.copy()
    ctx.update({"request": request})
    template = templates.get_template(template_name)  # jinja2.environment.Template
    html_string = template.render(ctx)  # msh fahem deh aw m7tag ashofha
    # can return any html response
    response = responses.HTMLResponse(html_string, status_code)
    # response = templates.TemplateResponse(template_name, ctx, status_code=status_code)
    # print(request.cookies)
    # response.set_cookie(key='test',value='123', httponly=True) # httponly=True to avoid client side tampering of the cookies and get it from the Request
    # to avoid compare dict keys to int (TypeError: '>' not supported between instances of 'dict_keys' and 'int')
    if len(list(cookies.keys())) > 0:
        for k, v in cookies.items():
            response.set_cookie(k, v, httponly=True)

    return response


def redirect(request: Request, path: str, cookies: dict = {}, remove_session: bool = False):
    # status code 302 is to avoid method not allowed in case of post request instead of 302 (check notes for more details)
    response = responses.RedirectResponse(path, status_code=302)
    for k, v in cookies.items():
        response.set_cookie(k, v, httponly=True)

    if remove_session is True:
        response.set_cookie(key='session_ended', value=1, httponly=True)
        response.delete_cookie('session_id')

    return response

def get_object_or_404(ClassInstance, **kwargs):
    try:
        obj = ClassInstance.objects.get(**kwargs)
    except DoesNotExist: 
        raise GenericException(status_code=404, detail='Object isnot found')
    except MultipleObjectsReturned:
        raise GenericException(status_code=400, detail='multiple objects returned')
    except:
        raise GenericException(status_code=500, detail='Something went wrong')
    
    return obj