import asyncio

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config import TEMPLATE_DIRECTORY

router = APIRouter(
    prefix="",
    tags=["home"],
    responses={404: {"description": "Not found"}},
)

task = None

async def greet_every_two_seconds():
    try:
        while True:
            print("Hello World")
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        print("Task cancelled!")
        raise  # important: re-raise

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