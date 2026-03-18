from fastapi import Response
import uuid
from app.config import COOKIE_SESSION_KEY, SESSION_LIFESPAN_SECONDS
from app.modules.auth.AuthRepository import AuthRepository
from app.modules.auth.data_classes.Session import Session
from app.modules.user.UserRepository import UserRepository
from time import time


class AuthService:
    def __init__(self, user_repository, auth_repository):
        self.user_repository : UserRepository = user_repository
        self.auth_repository: AuthRepository = auth_repository
        
    async def get_all(self):
        return await self.user_repository.get_all()
    
    async def login(self, username, password) -> Response:
        # prepare base response of fail of login
        response = Response()
        response.status_code = 302
        response.headers.append("Location", "/login")
        user = await self.user_repository.get_by_username(username)
        
        if(not user):
            return response
        
        if(user.password != password):
            return response
        
        # login successfull redirect to home page
        session_token = uuid.uuid4().hex
        await self.auth_repository.create_session(user.id, session_token)
        
        response.set_cookie(key=COOKIE_SESSION_KEY, value=session_token, secure=True, httponly=True, samesite="strict")
        response.headers["Location"] = "/"
        return response
    
    async def get_user_id_from_session(self, session_token):
        session = await self.auth_repository.get_session(session_token)
        
        if(self.__is_session_valid(session)):
            await self.auth_repository.refresh_session(session_token)
            return session.user_id
        elif(session_token): # if session not valid but still got a token, delete what may be in the sessions table
            await self.auth_repository.delete_session(session_token)

        return None
    
    def __is_session_valid(self, session : Session ):
        last_access_timestamp = int(session.last_accessed_at.timestamp())
        now_timestamp =  int(time())    
        elapsed = now_timestamp - last_access_timestamp
        
        return session and elapsed < SESSION_LIFESPAN_SECONDS