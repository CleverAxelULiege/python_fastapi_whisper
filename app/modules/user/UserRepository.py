from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool
from app.modules.user.data_classes.User import User

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
            

                
    async def get_by_id(self, user_id):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute("SELECT * FROM users WHERE id =  %s LIMIT 1", [user_id])
                return await cur.fetchone()