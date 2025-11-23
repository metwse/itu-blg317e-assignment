from src.app import create_app

import os
import asyncpg
import asyncio
from dotenv import load_dotenv
import uvicorn
from asgiref.wsgi import WsgiToAsgi


load_dotenv()

HOST = os.environ.get('HOST', "127.0.0.1")
PORT = int(os.environ.get('PORT', 6767))
LOG_LEVEL = os.environ.get('LOG_LEVEL', "info")
DEBUG = bool(os.environ.get('DEBUG'))
DATABASE_URL = os.environ.get('DATABASE_URL')
INTERNAL_ACCESS_TOKEN = os.environ.get('INTERNAL_ACCESS_TOKEN')

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable must be set in order "
                     "to run the backend.")


async def main():
    pool = await asyncpg.create_pool(DATABASE_URL)

    flask_app = create_app(pool, internal_access_token=INTERNAL_ACCESS_TOKEN)

    app = WsgiToAsgi(flask_app)

    config = uvicorn.Config(
        app,
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        reload=DEBUG
    )

    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bye!")
