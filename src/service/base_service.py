from src.repo.base_repo import BaseRepo

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel


T = TypeVar('T', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)
C = TypeVar('C', bound=BaseModel)


class BaseService(Generic[T, U, C]):
    """The base class for the Service Layer, acting as a bridge between the
    Handlers (Controllers) and the Repositories (Data Access Layer).

    Attributes:
        repo (BaseRepo): The injected repository instance for database
                         operations.
        model_types (tuple): References to the generic types (Entity,
                             UpdateDTO, CreateDTO) used for runtime type
                             checking or instantiation.
    """

    def __init__(self, repo: BaseRepo[T, U, C]):
        """Initializes the service with a specific repository.

        Args:
            repo: An instance of a repository that matches the generic types T,
                  U, and C.
        """
        self.repo = repo
        self.model_types = repo.model_types

    async def get(self, keys: List[Any]) -> Optional[T]:
        return await self.repo.get_by_keys(keys)

    async def list(self, limit: int, offset: int) -> List[T]:
        return await self.repo.list(limit, offset)

    async def create(self, create_dto: C) -> Optional[dict]:
        return await self.repo.insert(create_dto)

    async def update(self, update_dto: U, keys: List[Any]) -> Optional[dict]:
        return await self.repo.update(keys, update_dto)

    async def delete(self, keys: List[Any]) -> Optional[dict]:
        return await self.repo.delete(keys)
