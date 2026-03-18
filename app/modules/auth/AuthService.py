from fastapi import Response
import uuid
from app.config import COOKIE_SESSION_KEY
from app.modules.user.UserRepository import UserRepository


class AuthService:
    def __init__(self, user_repository):
        self.user_repository : UserRepository = user_repository
        
    async def get_all(self):
        return await self.user_repository.get_all()
    
    async def login(self, username, password) -> Response:
        response = Response()
        response.status_code = 302
        response.headers.append("Location", "/login")
        user = await self.user_repository.get_by_username(username)
        
        if(not user):
            return response
        
        if(user.password != password):
            return response
        
        session_token = uuid.uuid4().hex
        await self.user_repository.create_session(user.id, session_token)
        
        response.set_cookie(key=COOKIE_SESSION_KEY, value=session_token, secure=True, httponly=True, samesite="strict")
        response.headers["Location"] = "/"
        return response