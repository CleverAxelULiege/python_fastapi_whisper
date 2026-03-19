
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config import TEMPLATE_DIRECTORY


def get_transcription_controller():

    router = APIRouter(
        prefix="/transcription",
        tags=["transcription"],
        responses={404: {"description": "Not found"}},
    )

    @router.get("", response_class=HTMLResponse)
    async def read_transcription_index(request: Request):
        return TEMPLATE_DIRECTORY.TemplateResponse(
            request=request,
            name="transcription/index.html",
        )
        
    read_transcription_index

    return router