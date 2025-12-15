from src.app import create_app
from src.state import from_env

import os
import asyncio
from dotenv import load_dotenv
import uvicorn
from asgiref.wsgi import WsgiToAsgi


load_dotenv()

HOST = os.environ.get('HOST', "127.0.0.1")
PORT = int(os.environ.get('PORT', 6767))
LOG_LEVEL = os.environ.get('LOG_LEVEL', "info")
DEBUG = bool(os.environ.get('DEBUG'))


async def main():
    state = await from_env()

    flask_app = create_app(state)

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
