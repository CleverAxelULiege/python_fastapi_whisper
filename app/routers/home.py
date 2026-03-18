from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config import TEMPLATE_DIRECTORY

router = APIRouter(
    prefix="",
    tags=["home"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def read_home_page(request:Request):
    return TEMPLATE_DIRECTORY.TemplateResponse(
        request=request, name="home/index.html"
    )