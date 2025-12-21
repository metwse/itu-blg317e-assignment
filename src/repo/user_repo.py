from . import BaseRepo

from src.dto import UserCreateDto, UserUpdateDto
from src.entities import User


class UserRepo(BaseRepo[User, UserUpdateDto, UserCreateDto]):
    def __init__(self, pool):
        super().__init__(pool, 'users', ['id'],
                         (User, UserUpdateDto, UserCreateDto))

    async def get_all_users(self):  # MANAGEMENT
        return await self.fetch_raw(
            "SELECT id, email, name FROM users ORDER BY id DESC"
        )

    async def get_user_by_email(self, email: str):  # MANAGEMENT
        """Fetch a user by email for authentication.

        Args:
            email: The user's email address.

        Returns:
            The user record with id, email, password, name if found.
        """
        return await self.fetchrow_raw(
            """
            SELECT id, email, password, name FROM users
            WHERE email = $1
            """,
            email
        )

    async def get_user_by_id(self, user_id: int):  # MANAGEMENT
        """Fetch a user by ID.

        Args:
            user_id: The user's ID.

        Returns:
            The user record with id, email, name if found.
        """
        return await self.fetchrow_raw(
            """
            SELECT id, email, name FROM users
            WHERE id = $1
            """,
            user_id
        )

    async def create_user(self, email, password, name):  # MANAGEMENT
        return await self.fetchrow_raw(
            """
            INSERT INTO users (email, password, name) VALUES ($1, $2, $3)
            RETURNING id
            """,
            email, password, name
        )

    async def delete_user(self, id):  # MANAGEMENT
        return await self.fetchrow_raw(
            """
            DELETE FROM users WHERE id = $1
            RETURNING id
            """,
            id
        )

    async def reset_password(self, id, password):  # MANAGEMENT
        return await self.fetchrow_raw(
            """
            UPDATE users SET password = $1 WHERE id = $2
            RETURNING id
            """,
            password, id
        )
