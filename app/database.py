from psycopg_pool import AsyncConnectionPool
#postgresql://user:password@localhost/dbname"
pool = AsyncConnectionPool(
    "postgresql://postgres:admin@localhost/whisper",
    min_size=1,
    max_size=10,
    open=False
)