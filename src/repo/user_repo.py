from . import BaseRepo

from src.dto import UserCreateDto, UserUpdateDto
from src.entities import User


class UserRepo(BaseRepo[User, UserUpdateDto, UserCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'users', ['id'],
                         (User, UserUpdateDto, UserCreateDto))

    async def get_all_users(self):
        return await self.fetch_raw(
            "SELECT id, email, name FROM users ORDER BY id DESC"
        )

    async def create_user(self, email, password, name):
        return await self.fetchrow_raw(
            """
            INSERT INTO users (email, password, name) VALUES ($1, $2, $3)
            RETURNING id
            """,
            email, password, name
        )

    async def delete_user(self, id):
        return await self.fetchrow_raw(
            """
            DELETE FROM users WHERE id = $1
            RETURNING id
            """,
            id
        )

    async def reset_password(self, id, password):
        return await self.fetchrow_raw(
            """
            UPDATE users SET password = $1 WHERE id = $2
            RETURNING id
            """,
            password, id
        )
