from psycopg_pool import AsyncConnectionPool

from app.config import DATABASE_PORT, DATABASE_USERNAME, DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD
pool = AsyncConnectionPool(
    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
    min_size=1,
    max_size=10,
    open=False
)