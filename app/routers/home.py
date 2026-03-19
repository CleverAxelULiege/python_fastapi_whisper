import asyncio

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent

from app.config import TEMPLATE_DIRECTORY

router = APIRouter(
    prefix="",
    tags=["home"],
    responses={404: {"description": "Not found"}},
)


async def greet_every_two_seconds():
    try:
        while True:
            print("Hello World")
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        print("Task cancelled!")
        raise
    
@router.get("/stream", response_class=EventSourceResponse)
async def read_stream():
    print("client connected to stream")
    words = [1, 2, 3, 4, 5]
    for word in words:
        await asyncio.sleep(3)
        yield ServerSentEvent(data=word, event="token")
        
    yield ServerSentEvent(raw_data="[DONE]", event="done")

@router.get("/sse", response_class=HTMLResponse)
async def read_sse(request:Request):
    return TEMPLATE_DIRECTORY.TemplateResponse(
        request=request, name="home/sse.html"
    )
    
@router.get("/", response_class=HTMLResponse)
async def read_home_page(request:Request):
    return TEMPLATE_DIRECTORY.TemplateResponse(
        request=request, name="home/index.html"
    )
    
@router.get("/test")
async def read_test(request:Request):
    task = asyncio.create_task(greet_every_two_seconds())
    request.app.state.task = task
    print(task)
    
    return {"msg" : "hello world"}

# @router.get("/abort")
# async def read_abort(request:Request):
#     print(request.app.state.task)
#     return {"msg" : "abort"}