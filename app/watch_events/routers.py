
from fastapi import APIRouter, Request

from .schemas import WatchEventSchema
from .models import WatchEvent

watch_event_router = APIRouter()


@watch_event_router.post("/watch-event", response_model=WatchEventSchema)
def watch_event_view(request: Request,
                     watch_event: WatchEventSchema):
    '''
    * the variable naming of data doesn't matter 
    * fastapi converts the string into json in the background so no need for json.loads(dataString)

    '''
    ######## how come it know the request.user if is_authenticated is true and is_authenticated is false ???? ############
    ### I need an explanation due to the JWTBACKENDCOOKIE middleware we added at the beginning
    # validated_data = watch_event.model_dump()
    # data = validated_data.copy()
    # print(data)
    # saved = False
    # if request.user.is_authenticated is True:
    #     duration = data.get("duration")
    #     start_time = data.get("startTime")
    #     current_time = data.get("currentTime")
    #     completed = start_time >= current_time if current_time else False
    #     WatchEvent.objects.create(
    #         host_id=data.get("videoId"),
    #         user_id=request.user.username,
    #         start_time=start_time,
    #         end_time=current_time,
    #         duration=duration,
    #         complete=completed
    #     )
    #     saved = True

    validated_data = watch_event.model_dump()
    data = validated_data.copy()
    if request.user.is_authenticated is False:
        print("NOT A VIDEO MEMBERSHIP")
        return watch_event
    obj_in_db: WatchEvent = WatchEvent.objects(user_id=request.user.username,
                                               host_id=watch_event.host_id).allow_filtering().first()
    if obj_in_db:
        print("UPDATING ----", watch_event.start_time)
        obj_in_db.start_time = watch_event.start_time
        obj_in_db.end_time = watch_event.end_time
        obj_in_db.save()
        obj_in_db.complete = WatchEvent.is_completed
        obj_in_db.save()
        print(obj_in_db)
        return validated_data

    data.update({"user_id": request.user.username})
    obj = WatchEvent.objects.create(**data)
    print("SAVING OBJECT ==> ,", obj)
    return validated_data


'''
inspecting request.__dict__ and it displayed the following
{
'scope': {'type': 'http', 
            'asgi': {'version': '3.0', 'spec_version': '2.3'}, 
            'http_version': '1.1', 
            'server': ('127.0.0.1', 8000), 
            'client': ('127.0.0.1', 40832), 
            'scheme': 'http', 
            'method': 'POST', 
            'root_path': '', 
            'path': '/watch-event', 
            'raw_path': b'/watch-event', 
            'query_string': b'', 
            'headers': [
                (b'host', b'127.0.0.1:8000'), 
                (b'connection', b'keep-alive'), 
                (b'content-length', b'49'), 
                (b'sec-ch-ua', b'"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'), 
                (b'sec-ch-ua-platform', b'"Linux"'), 
                (b'sec-ch-ua-mobile', b'?0'),
                (b'user-agent', b'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'), 
                (b'content-type', b'application/json'), 
                (b'accept', b'*/*'), 
                (b'origin', b'http://127.0.0.1:8000'), 
                (b'sec-fetch-site', b'same-origin'), 
                (b'sec-fetch-mode', b'cors'), 
                (b'sec-fetch-dest', b'empty'), 
                (b'referer', b'http://127.0.0.1:8000/videos/-D6G2a1M784'), 
                (b'accept-encoding', b'gzip, deflate, br'), 
                (b'accept-language', b'en-US,en;q=0.9'), 
                (b'cookie', b'session_ended=1; session_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTgyMDM4MWUtNzNiZS0xMWVlLWIwNTEtZTkxZjAyMzQ5YjYxIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjk5NzY2NDczLCJleHAiOjE2OTk3NjY1MzN9.tH-w1b9SCNC7VBbWMUFmDxylxAQtprsTytGl7YyEP6k')
            ], 
            'state': {}, 
            'app': <fastapi.applications.FastAPI object at 0x7ff9adb6ffa0>, 
            'auth': <starlette.authentication.AuthCredentials object at 0x7ff9ab3fbfa0>, 
            'user': <starlette.authentication.UnauthenticatedUser object at 0x7ff9ab391f00>, 
            'fastapi_astack': <contextlib.AsyncExitStack object at 0x7ff9ab391ed0>, 
            'router': <fastapi.routing.APIRouter object at 0x7ff9adba44c0>, 
            'endpoint': <function watch_event_view at 0x7ff9ab4f89d0>, 
            'path_params': {}, 
            'route': APIRoute(path='/watch-event', name='watch_event_view', methods=['POST'])}, 
            '_receive': <bound method RequestResponseCycle.receive of <uvicorn.protocols.http.h11_impl.RequestResponseCycle object at 0x7ff9ab391ba0>>, 
            '_send': <function ExceptionMiddleware.__call__.<locals>.sender at 0x7ff9ab4f9ab0>, 
            '_stream_consumed': True, 
            '_is_disconnected': False, 
            '_form': None, 
            '_body': b'{"currentTime":41.372372,"videoId":"-D6G2a1M784"}', 
            '_headers': Headers({'host': '127.0.0.1:8000', 'connection': 'keep-alive', 'content-length': '49', 'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'sec-ch-ua-platform': '"Linux"', 'sec-ch-ua-mobile': '?0', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 
            'content-type': 'application/json', 'accept': '*/*', 'origin': 'http://127.0.0.1:8000', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'http://127.0.0.1:8000/videos/-D6G2a1M784', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'cookie': 'session_ended=1; session_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTgyMDM4MWUtNzNiZS0xMWVlLWIwNTEtZTkxZjAyMzQ5YjYxIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjk5NzY2NDczLCJleHAiOjE2OTk3NjY1MzN9.tH-w1b9SCNC7VBbWMUFmDxylxAQtprsTytGl7YyEP6k'}),
            '_json': {'currentTime': 41.372372, 'videoId': '-D6G2a1M784'}, 
            '_query_params': QueryParams(''), 
            '_cookies': {'session_ended': '1', 'session_id': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTgyMDM4MWUtNzNiZS0xMWVlLWIwNTEtZTkxZjAyMzQ5YjYxIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjk5NzY2NDczLCJleHAiOjE2OTk3NjY1MzN9.tH-w1b9SCNC7VBbWMUFmDxylxAQtprsTytGl7YyEP6k'}
}
'''
