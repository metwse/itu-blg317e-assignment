from .repo.country_repo import CountryRepo
from .app import create_app
import asyncpg
import os
import asyncio
from dotenv import load_dotenv
<<<<<<< HEAD
load_dotenv()


HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 6767))
DEBUG = bool(os.environ.get("DEBUG"))
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://dbuser:insecure-password_NO-NOT-EXPOSE-THIS-DB-TO-PUBLIC@localhost:2345/blg317e")
=======


load_dotenv()
>>>>>>> upstream/main

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 6767))
DEBUG = bool(os.environ.get("DEBUG"))
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable must be set in order"
                     "to run the backend.")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
<<<<<<< HEAD
    pool = loop.run_until_complete(asyncpg.create_pool(DATABASE_URL))
    repo = CountryRepo(pool)
    app = create_app(repo, loop)
=======

    pool = loop.run_until_complete(asyncpg.create_pool(DATABASE_URL))

    repo = CountryRepo(pool)

    app = create_app(repo, loop)

>>>>>>> upstream/main
    app.run(host=HOST, port=PORT, debug=DEBUG)
