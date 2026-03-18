from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from app.config import TEMPLATE_DIRECTORY
from app.modules.auth.AuthService import AuthService

router = APIRouter(
    prefix="",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

def get_auth_controller(auth_service:AuthService):

    router = APIRouter(
        prefix="",
        tags=["auth"],
        responses={404: {"description": "Not found"}},
    )
    
    @router.get("/test")
    async def read_test(request: Request):
        return await auth_service.get_all()

    @router.get("/login", response_class=HTMLResponse)
    async def read_login_page(request: Request):
        return TEMPLATE_DIRECTORY.TemplateResponse(
            request=request,
            name="home/login.html",
        )

    @router.post("/login", response_class=HTMLResponse) 
    async def post_login_page(request: Request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        
        if(not username or not password):
            return RedirectResponse("/login", status_code=302)
        
        response_auth = await auth_service.login(username, password)
        return response_auth
            
        
        
            

    @router.get("/logout")
    async def logout():
        response = RedirectResponse("/", status_code=302)
        response.delete_cookie("access_token")
        return response

    logout and post_login_page and read_login_page and read_test
    return router