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


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    pool = loop.run_until_complete(asyncpg.create_pool(DATABASE_URL))
    repo = CountryRepo(pool)
    app = create_app(repo, loop)
    app.run(host=HOST, port=PORT, debug=DEBUG)
