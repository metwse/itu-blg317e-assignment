from src import AppError, AppErrorType
from src.service.base_service import BaseService
from src.handlers import json

from typing import Generic, TypeVar
from pydantic import BaseModel

from flask import request, jsonify


T = TypeVar('T', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)
C = TypeVar('C', bound=BaseModel)


class BaseHandler(Generic[T, U, C]):
    """Base controller class for handling HTTP requests.

    This class serves as the interface between the HTTP layer (Flask) and the
    Business Logic layer (Service). It standardizes the handling of CRUD
    operations by:
    - Parsing and validating incoming JSON requests against Pydantic DTOs.
    - Formatting outgoing responses as JSON.
    - Mapping application errors to appropriate HTTP status codes.

    Attributes:
        service (BaseService): The service instance handling business logic.
        update_dto_class (Type[U]): The Pydantic model class used for
                                    validating update requests.
        create_dto_class (Type[C]): The Pydantic model class used for
                                    validating creation requests.
    """

    def __init__(self, service: BaseService[T, U, C]):
        """Initializes the handler with a specific service instance.

        It extracts the DTO classes (UpdateDTO and CreateDTO) from the
        service's model definitions to be used later for runtime JSON
        validation in `create` and `update` methods.

        Args:
            service: An instance of BaseService configured for a specific
                     entity type.
        """

        self.service = service

        self.update_dto_class = service.model_types[1]
        self.create_dto_class = service.model_types[2]

    async def list(self):
        try:
            limit = int(request.args.get("limit", 100))
            offset = int(request.args.get("offset", 0))
        except ValueError:
            raise AppError(AppErrorType.VALIDATION_ERROR,
                           "limit and offset must be integers")

        return jsonify(
            [
                i.model_dump()
                for i in await self.service.list(limit, offset)
            ]
        )

    async def get(self, *keys):
        res = await self.service.get([*keys])

        if res is not None:
            return jsonify(res.model_dump())
        else:
            raise AppError(AppErrorType.NOT_FOUND, "entity not found")

    async def create(self):
        data = json()

        model = self.create_dto_class(**data)

        try:
            res = await self.service.create(model)
        except Exception:
            raise AppError(AppErrorType.ALREADY_EXITS,
                           "a record with provided keys already exits")

        return jsonify(res), 201

    async def update(self, *keys):
        data = json()

        update_dto = self.update_dto_class(**data)

        res = await self.service.update(update_dto, [*keys])

        if res is not None:
            return jsonify(res)
        else:
            raise AppError(AppErrorType.VALIDATION_ERROR, "no field to update")

    async def delete(self, *keys):
        return jsonify(await self.service.delete([*keys]))
