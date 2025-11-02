from .repo.country_repo import CountryRepo
from .app import create_app
import asyncpg
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 6767))
DEBUG = bool(os.environ.get("DEBUG"))
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://dbuser:insecure-password_NO-NOT-EXPOSE-THIS-DB-TO-PUBLIC@localhost:2345/blg317e")


async def setup_repo():
    pool = await asyncpg.create_pool(DATABASE_URL)
    return CountryRepo(pool)


if __name__ == "__main__":
    repo = asyncio.run(setup_repo())
    app = create_app(repo)
    app.run(host=HOST, port=PORT, debug=DEBUG)
