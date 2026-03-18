from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool
from app.modules.auth.Session import Session

class AuthRepository:
    def __init__(self, pool):
        self.pool: AsyncConnectionPool = pool

    async def get_session(self, session_token):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Session)) as cur:
                await cur.execute("SELECT * FROM sessions WHERE token ILIKE %s LIMIT 1", [session_token])
                return await cur.fetchone()
            
    