from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import COOKIE_SESSION_KEY, SESSION_LIFESPAN_SECONDS
from app.modules.auth.AuthService import AuthService
from app.modules.user.UserRepository import UserRepository

# Middleware check if a session is being set and refresh it
class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, user_repository: UserRepository, auth_service: AuthService, cookie_name: str = COOKIE_SESSION_KEY):
        super().__init__(app)
        self.cookie_name = cookie_name
        self.auth_service = auth_service
        self.user_repository = user_repository

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/public"):
            return await call_next(request)
    
        request.state.user = None
        session_token = request.cookies.get(self.cookie_name)
        current_session = None
        
        if session_token:
            current_session = await self.auth_service.get_current_session(session_token)
            if(current_session):
                request.state.user = await self.user_repository.get_by_id(current_session.user_id)

        response = await call_next(request)
        if(current_session):
            response.set_cookie(key=COOKIE_SESSION_KEY, value=current_session.token, secure=True, httponly=True, samesite="strict", expires=datetime.now(timezone.utc) + timedelta(seconds=SESSION_LIFESPAN_SECONDS))
        return response

