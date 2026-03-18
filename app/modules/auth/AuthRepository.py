from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool
from app.modules.auth.data_classes.Session import Session

class AuthRepository:
    def __init__(self, pool):
        self.pool: AsyncConnectionPool = pool

    async def get_session(self, session_token):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Session)) as cur:
                await cur.execute("SELECT * FROM sessions WHERE token ILIKE %s LIMIT 1", [session_token])
                return await cur.fetchone()
            
    async def create_session(self, user_id, session_token):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO sessions (token, user_id, last_accessed_at) VALUES (%s, %s, CURRENT_TIMESTAMP(0)::TIMESTAMP WITHOUT TIME ZONE)",
                    [session_token, user_id]
                )    
                        
    async def refresh_session(self, session_token):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE sessions SET last_accessed_at = CURRENT_TIMESTAMP(0)::TIMESTAMP WITHOUT TIME ZONE WHERE token = %s",
                    [session_token]
                )   
                         
    async def delete_session(self, session_token):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "DELETE FROM sessions WHERE token = %s",
                    [session_token]
                )            
    