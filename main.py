from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.middlewares.AuthMiddleware import AuthMiddleware
from app.middlewares.SessionMiddleware import SessionMiddleware

from app.modules.user.UserRepository import UserRepository

from app.modules.auth.AuthService import AuthService
from app.modules.auth.AuthRepository import AuthRepository

from app.modules.transcription.TranscriptionController import get_transcription_controller
from app.modules.auth.AuthController import get_auth_controller
from app.routers import home

from app.config import PUBLIC_FILE_DIRECTORY
from app.database import pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Connecting to database...")
        await pool.open()
    except Exception as e:
        print("DB not available:", e)
    yield
    # Clean up 
    
    
auth_repo = AuthRepository(pool)
user_repo = UserRepository(pool)

auth_service = AuthService(user_repo, auth_repo)

app = FastAPI(lifespan=lifespan )
app.mount("/public", PUBLIC_FILE_DIRECTORY, name="public")
app.include_router(home.router)
app.include_router(get_transcription_controller())
app.include_router(get_auth_controller(auth_service))

app.add_middleware(AuthMiddleware)
app.add_middleware(SessionMiddleware, user_repository=user_repo, auth_service=auth_service)







