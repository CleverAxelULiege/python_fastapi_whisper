from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from app.config import COOKIE_SESSION_KEY, SESSION_LIFESPAN_SECONDS, TEMPLATE_DIRECTORY
from app.modules.auth.AuthService import AuthService
from app.modules.auth.consts.LoginResult import LoginResult
from app.modules.auth.depends.is_logged_in import is_logged_in

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
    async def read_login_page(request: Request, is_logged_in=Depends(is_logged_in)):
        if(is_logged_in):
            return RedirectResponse("/", status_code=302)
        
        return TEMPLATE_DIRECTORY.TemplateResponse(
            request=request,
            name="home/login.html",
        )

    @router.post("/login", response_class=HTMLResponse) 
    async def post_login_page(request: Request, is_logged_in=Depends(is_logged_in)):
        
        if(is_logged_in):
            return RedirectResponse("/", status_code=302)
        
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        
        if(not username or not password):
            return RedirectResponse("/login", status_code=302)
        
        response = Response(status_code=302)
        result, session_token = await auth_service.login(username, password)
        if (result == LoginResult.SUCCESS):
            response.set_cookie(
                key=COOKIE_SESSION_KEY,
                value=session_token,
                secure=True,
                httponly=True,
                samesite="strict",
                expires=datetime.now(timezone.utc) + timedelta(seconds=SESSION_LIFESPAN_SECONDS)
            )
            response.headers["Location"] = "/"
        else:
            response.headers["Location"] = "/login"
        return response
            
        
        
            

    @router.get("/logout")
    async def logout(request: Request):
        session_token = request.cookies.get(COOKIE_SESSION_KEY)
        await auth_service.delete_session(session_token)
        
        response = RedirectResponse("/", status_code=302)
        response.delete_cookie(COOKIE_SESSION_KEY)
        return response

    logout and post_login_page and read_login_page and read_test
    return router