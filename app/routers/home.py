import asyncio
import json
import threading

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent
from faster_whisper import WhisperModel

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
    
def whisper_test(stop_event:threading.Event, queue:asyncio.Queue):
    try:
        model = WhisperModel(
            r"C:\Users\Public\whisper_models\faster-whisper-small",
            device="cpu",
            compute_type="int8",
            cpu_threads=  4,
            num_workers=2
        )
        
        segments, info = model.transcribe(
                r"C:\Users\clever\Documents\python\faster-whisper\audio\audio_tf1.mp3",
                language="fr",
                task="transcribe",
                beam_size=1,
                vad_filter=True
            )
        
        for segment in segments:
            if(stop_event.is_set()):
                return
            text = segment.text.strip()
            queue.put_nowait(text)
            # print(text)
            
    except asyncio.CancelledError:
        print("Task cancelled!")
        raise
    
@router.get("/stream", response_class=EventSourceResponse)
async def read_stream(request:Request):
    queue = asyncio.Queue()
    stop_event = threading.Event()
    task = asyncio.create_task(asyncio.to_thread(whisper_test, stop_event, queue))
    
    request.app.state.task = task
    request.app.state.stop = stop_event
    
    while(True):
        msg = await queue.get()
        yield ServerSentEvent(data=msg, event="token", retry=15000)
        
        if(task.done()):
            break
    # print("client connected to stream")
    # words = ["héhéhéhéhéhéhéhéhé", "àààààààààà", "çççççççççççççç"]
    # for word in words:
    #     yield ServerSentEvent(data=json.dumps({"msg" : word}, ensure_ascii=False), event="token")
        
    yield ServerSentEvent(raw_data="[DONE]", event="done")

@router.get("/sse", response_class=HTMLResponse)
async def read_sse(request:Request):
    return TEMPLATE_DIRECTORY.TemplateResponse(
        request=request, name="home/sse.html"
    )
    
@router.get("/ajax")
async def read_ajax():
    return {"msg" : "héhéhéhéhé"}
    
@router.get("/", response_class=HTMLResponse)
async def read_home_page(request:Request):
    return TEMPLATE_DIRECTORY.TemplateResponse(
        request=request, name="home/index.html"
    )
    
@router.get("/test")
async def read_test(request:Request):
    # task = asyncio.create_task(asyncio.to_thread(whisper_test))
    # request.app.state.task = task
    # print(task)
    
    return {"msg" : "hello world"}

# @router.get("/abort")
# async def read_abort(request:Request):
#     print(request.app.state.task)
#     return {"msg" : "abort"}