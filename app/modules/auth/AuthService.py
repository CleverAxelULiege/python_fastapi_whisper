import uuid
from app.config import SESSION_LIFESPAN_SECONDS
from app.modules.auth.AuthRepository import AuthRepository
from app.modules.auth.consts.LoginResult import LoginResult
from app.modules.auth.data_classes.Session import Session
from app.modules.user.UserRepository import UserRepository
from time import time


class AuthService:
    def __init__(self, user_repository, auth_repository):
        self.user_repository : UserRepository = user_repository
        self.auth_repository: AuthRepository = auth_repository
        
    async def get_all(self):
        return await self.user_repository.get_all()
    
    async def login(self, username, password):
        user = await self.user_repository.get_by_username(username)
        
        if not user:
            return LoginResult.USER_NOT_FOUND, None
        
        if user.password != password:
            return LoginResult.INVALID_PASSWORD, None
        
        
        
        session_token = uuid.uuid4().hex
        await self.auth_repository.create_session(user.id, session_token)
        
        return LoginResult.SUCCESS, session_token
    
    async def get_current_session(self, session_token):
        session = await self.auth_repository.get_session(session_token)
        
        if(self.__is_session_valid(session)):
            await self.auth_repository.refresh_session(session_token)
            return session
        elif(session_token): # if session not valid but still got a token, delete what may be in the sessions table
            await self.auth_repository.delete_session(session_token)

        return None
    
    def __is_session_valid(self, session : Session ):
        if(not session):
            return False
        last_access_timestamp = int(session.last_accessed_at.timestamp())
        now_timestamp =  int(time())    
        elapsed = now_timestamp - last_access_timestamp
        
        return elapsed < SESSION_LIFESPAN_SECONDS
    
    async def delete_session(self, session_token):
        await self.auth_repository.delete_session(session_token)