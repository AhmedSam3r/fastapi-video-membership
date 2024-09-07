from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse

from app.shortcuts import render, redirect, get_object_or_404
from app.decorators import login_required
from .schemas import VideoCreateSchema
from app import utils 
from .models import Video

from app.watch_events.models import WatchEvent

video_router = APIRouter()
# it's good since we added it in the main include_router()
# router = APIRouter(prefix='/videos')


@video_router.get('/create', response_class=HTMLResponse)
@login_required
async def video_create_view(request: Request):
    return render(request, "videos/create.html", {})


@video_router.post('/create', response_class=HTMLResponse)
@login_required
async def video_create_post_view(
        request: Request,
        title: str = Form(...),
        url: str = Form(...),
):
    raw_data = {
        "url": url,
        "user_id": request.user.username,
        "title": title
    }
    data, errors = utils.valid_schema_or_error(raw_data, VideoCreateSchema)
    context = {
        "url": url,
        "data": data,
        "errors": errors
    }
    print("data = ", data)
    if len(errors) > 0:
        print("video_create_post_view errors = ", errors)
        return render(request, "videos/create.html", context, status_code=400)

    video_path = data.get('path') or "/videos/create"
    return redirect(request, video_path)


@video_router.get('/list', response_class=HTMLResponse)
async def video_list_view(request: Request):
    videos = Video.objects.all().limit(10)
    # video_data = [{'url': video.url, 'host_id': video.host_id} for video in videos]
    # return JSONResponse(content=video_data)
    context = {
        "videos": videos
    }
    return render(request, "videos/list.html", context)


@video_router.get('/{host_id}', response_class=HTMLResponse)
async def video_list_view(request: Request, host_id: str):
    video = get_object_or_404(Video, host_id=host_id)
    # newlw added part of resume time
    start_time = 0
    if request.user.is_authenticated:
        start_time = WatchEvent.get_resume_time(host_id, request.user.username)

    context = {
        "video": video,
        "host_id": host_id,
        "start_time": round(start_time, 2)
    }
    return render(request, "videos/detail.html", context)
