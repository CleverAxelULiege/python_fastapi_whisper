from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import COOKIE_SESSION_KEY
from app.modules.auth.AuthService import AuthService
from app.modules.user.UserRepository import UserRepository

class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, user_repository: UserRepository, auth_service: AuthService, cookie_name: str = COOKIE_SESSION_KEY):
        super().__init__(app)
        self.cookie_name = cookie_name
        self.auth_service = auth_service
        self.user_repository = user_repository

    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        session_token = request.cookies.get(self.cookie_name)

        if session_token:
            user_id = await self.auth_service.get_user_id_from_session(session_token)
            if(user_id):
                request.state.user = await self.user_repository.get_by_id(user_id)

        response = await call_next(request)
        return response

