from dotenv import load_dotenv
import os
import asyncpg
import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.test_data import TEST_COUNTRIES  # noqa: E402

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://dbuser:insecure-password_NO-NOT-EXPOSE-THIS-DB-TO-PUBLIC@localhost:2345/blg317e")


async def init_database():
    print(f"Connecting to database...")
    pool = await asyncpg.create_pool(DATABASE_URL)

    async with pool.acquire() as conn:
        print("Loading test data...")
        for country in TEST_COUNTRIES:
            try:
                code_array = list(country["code"])
                await conn.execute(
                    "INSERT INTO countries (code, name, continent, lat, lng) VALUES ($1, $2, $3, $4, $5)",
                    code_array, country["name"], country.get("continent"),
                    country.get("lat"), country.get("lng")
                )
                print(f"  ✓ Added {country['name']}")
            except Exception as e:
                print(f"  ⚠ {country['name']}: {e}")

    await pool.close()
    print("\n✓ Database initialized!")


if __name__ == "__main__":
    asyncio.run(init_database())
