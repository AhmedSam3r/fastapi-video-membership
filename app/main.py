from fastapi import FastAPI, Request, Form, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import  AuthenticationMiddleware
from cassandra.cqlengine.management import sync_table
from starlette.authentication import requires

from . import config, db, utils, handlers
from .users.models import User
from .schemas.userschemas import *
from .shortcuts import render, redirect
from .decorators import login_required
from .handlers import * # noqa
from .backend import JWTCookieBackend

from .videos.models import Video
from .videos.routers import video_router

from .watch_events.models import WatchEvent
from .watch_events.routers import watch_event_router

from pydantic_core._pydantic_core import ValidationError

from app import app

import json
import pathlib

# app/ works on cross platform mac, win & linux
# resolve() returns the absolute path and the current file .../main.py and parent returns the parent path .../app 

# to run the app uvicorn {app.}main:main_app
# main_app = FastAPI()
# app = FastAPI()
DB_SESSION = None

settings = config.get_settings()

app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(video_router, prefix='/videos')
app.include_router(watch_event_router, prefix="/events")


@app.on_event("startup")
def on_startup():
    print("on startup hello world")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)
    sync_table(WatchEvent)


@app.get("/", response_class=HTMLResponse)
@requires(['authenticated'])
async def home(request: Request):
    # json data --> REST API, html not allowed to return
    # keyspace = settings.astradb_keyspace  # import from .env file
    # return {"key": "value", }
    # ValueError: context must include a "request" key
    if request.user.is_authenticated:
        print(request.user.__dict__)
        # after customizing our class to inherit SimpleUser class we can now get the email attribute
        return render(request, "dashboard.html", {'email_username': (request.user.email + ' ' + request.user.username)}, 200)
    context = {
        # older way of passing the request
        # 'request': request,
        'title': 'FASTAPI COURSE'}
    # return templates.TemplateResponse('home.html', context=context)
    return render(request, 'home.html', context=context)


@app.get("/account", response_class=HTMLResponse)
@login_required
async def account(request: Request):
    session_id = request.cookies.get('session_id')
    if session_id is None:
        raise HTTPException(status_code=400, detail='Not logged in, No session id')
    context = {
        'title': 'Account Page'}
    return render(request, 'account.html', context=context)


@app.get('/signup', response_class=HTMLResponse)
async def signup_get_view(request: Request):
    '''email and password variable names are the same as in the register.html form'''
    context = {
        # older way of passing the request
        # 'request': request,
        'title': 'signup Page'}

    # return templates.TemplateResponse('auth/register.html', context=context)
    # abstract method that uses the same old line
    return render(request, 'auth/register.html', context=context)


@app.post('/signup', response_class=HTMLResponse)
async def signup_post_view(request: Request,
                           email: str = Form(...),
                           password: str = Form(...),
                           password_confirmation: str = Form(...)):
    '''email and password variable names are the same as in the login.html form'''
    raw_data = {
        'email': email,
        'password': password,
        'password_confirmation': password_confirmation
    }
    data, errors = utils.valid_schema_or_error(raw_data, UserSignupSchema)
    context = {
        # older way of passing the request
            # 'request': request,
            'data': data,
            'errors': errors
        }
    status_code = 200 if len(errors) == 0 else 400
    # return templates.TemplateResponse('auth/register.html', context=context)
    return render(request, 'auth/register.html', context=context, status_code=status_code)


@app.get('/login', response_class=HTMLResponse)
async def login_get_view(request: Request,
                         next: str = Query('/', title='Next Page Path')):
    '''email and password variable names are the same as in the login.html form
        else you will get this error or similar one
        ==> {"detail":[{"type":"missing","loc":["body","password"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.4/v/missing"}]} # noqa: E501
        '''
    context = {
        # older way of passing the request
        # 'request': request,
        'title': 'Login Page',
        'next': next}
    # return templates.TemplateResponse('auth/login.html', context=context)
    return render(request, 'auth/login.html', context=context)


@app.post('/login', response_class=HTMLResponse)
async def login_post_view(request: Request,
                          next: str = Form(...),  
                          email: str = Form(...),
                          password: str = Form(...),
                          ):
    '''email and password variable names are the same as in the login.html form'''
    session_id: str = request.cookies.get("session_id")
    raw_data = {
        'email': email,
        'password': password,
        'logged_in': bool(session_id)
    }
    data, errors = utils.valid_schema_or_error(raw_data, UserLoginSchema)
    logged_in = True if data else False
    context = {
        # older way of passing the request
        # 'request': request,
        'data': data,
        'errors': errors,
        'logged_in': logged_in,
    }
    print("logged_in = ",logged_in)
    print("data = ", data)
    status_code = 200 if len(errors) == 0 else 400


    # request.cookies = data
    if status_code >= 400:
        return render(request, 'auth/login.html', context=context, status_code=status_code, cookies=data)

    # return templates.TemplateResponse('auth/login.html', context=context)
    # return render(request, 'auth/login.html', context=context, status_code=status_code, cookies=data)
    return redirect(request, next, cookies=data)


@app.get('/users')
async def users_list_view():
    # type is <class 'cassandra.cqlengine.query.ModelQuerySet'>
    query = User.objects.all().limit(10)
    return list(query)
