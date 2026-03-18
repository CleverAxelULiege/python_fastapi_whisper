from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

ROOT_DIR = Path("views").resolve().parent
TEMPLATE_DIRECTORY = Jinja2Templates(directory=ROOT_DIR / "views")
PUBLIC_FILE_DIRECTORY = StaticFiles(directory=ROOT_DIR / "public")
COOKIE_SESSION_KEY = "whisper_session_id"
SESSION_LIFESPAN_SECONDS = 3600
# pool = AsyncConnectionPool(
#     "postgresql://user:password@localhost/dbname",
#     min_size=1,
#     max_size=10
# )