"""Application state."""

from dataclasses import dataclass
import asyncpg
import os

from src.service import (
    ProviderService,
    EconomyService,
    PermissionService,
    IndicatorService,
    UserService
)


@dataclass
class State:
    """Application state container

    This class serves as the central registry for all singleton service
    instances and global configuration. It allows for clean dependency
    injection into request handlers, ensuring that every part of the app uses
    the same database pool and service logic.

    Also, fixtures are loaded using this state registry.
    """

    pool: asyncpg.pool.Pool
    provider_service: ProviderService
    user_service: UserService
    economy_service: EconomyService
    permission_service: PermissionService
    indicator_service: IndicatorService
    management_console_token: str
    jwt_secret: str
    internal_access_token: str | None


def bootstrap_state(pool,
                    management_console_token,
                    jwt_secret,
                    internal_access_token: str | None = None) -> State:
    """Bootstraps the application state by instantiating all services.

    Args:
        pool: The active asyncpg database connection pool.
        internal_access_token: The secret token for administrative access.
    """

    data = {'pool': pool}

    # Dynamic service instantiation loop
    for key, ServiceClass in State.__annotations__.items():
        # Assumes the type hint (ServiceClass) is the actual class object
        # and that its constructor accepts 'pool' as the first argument.
        if (key.endswith('service')):
            data[key] = ServiceClass(pool)

    data['internal_access_token'] = internal_access_token
    data['management_console_token'] = management_console_token
    data['jwt_secret'] = jwt_secret

    return State(**data)


async def from_env() -> State:
    """Factory function to initialize the State from environment variables.

    This helper handles the creation of the database connection pool using
    the `DATABASE_URL` environment variable and then bootstraps the state.

    Raises:
        ValueError: If `DATABASE_URL` is not found in environment variables.

    Returns:
        State: The initialized application state.
    """

    DATABASE_URL = os.environ.get('DATABASE_URL')
    INTERNAL_ACCESS_TOKEN = os.environ.get('INTERNAL_ACCESS_TOKEN')
    MANAGEMENT_CONSOLE_TOKEN = os.environ.get('MANAGEMENT_CONSOLE_TOKEN')
    JWT_SECRET = os.environ.get('JWT_SECRET')

    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable must be set in "
                         "order to run the backend.")

    if MANAGEMENT_CONSOLE_TOKEN is None:
        raise ValueError("MANAGEMENT_CONSOLE_TOKEN environment variable must "
                         "be set in order to control management console "
                         "access.")

    if JWT_SECRET is None:
        raise ValueError("A JWT_SECRET is required to sign web tokens.")

    # Create the connection pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    return bootstrap_state(pool,
                           MANAGEMENT_CONSOLE_TOKEN,
                           JWT_SECRET,
                           internal_access_token=INTERNAL_ACCESS_TOKEN)
