from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool
from app.modules.user.User import User

class UserRepository:
    def __init__(self, pool):
        self.pool: AsyncConnectionPool = pool

    async def get_all(self):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute("SELECT * FROM users")
                return await cur.fetchall()
            
    async def get_by_username(self, username)  : 
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute("SELECT * FROM users WHERE username ILIKE %s LIMIT 1", [username])
                return await cur.fetchone()
            
    async def create_session(self, user_id, session_token):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO sessions (token, user_id, last_accessed_at) VALUES (%s, %s, CURRENT_TIMESTAMP)",
                    [session_token, user_id]
                )
                
    async def get_by_id(self, user_id):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute("SELECT * FROM users WHERE id =  %s LIMIT 1", [user_id])
                return await cur.fetchone()