
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


# Middleware check if a session is being set and refresh it
class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        protected_paths = ["/transcription"]

        if any(request.url.path.lower().startswith(path) for path in protected_paths):
            if not request.state.user:
                return RedirectResponse("/login", status_code=302)

        return await call_next(request)
