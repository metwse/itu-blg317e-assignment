import asyncio
import sys
from pathlib import Path
import os
import asyncpg
import subprocess
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from test_data import TEST_COUNTRIES
from src.service.country_service import CountryService
from src.repo.country_repo import CountryRepo
def start_database():
    """Start the database container."""
    print("Starting database container...")

    # Check if Docker is running
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Docker is not running. Please start Docker Desktop.")
        print("See README.md for database setup instructions.")
        return False

    # Stop and remove existing container
    subprocess.run(["docker", "stop", "blg317e-test-db"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["docker", "rm", "blg317e-test-db"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Start new container
    result = subprocess.run([
        "docker", "run", "-d",
        "--name", "blg317e-test-db",
        "-p", "2345:5432",
        "blg317e-dev-db"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: Failed to start database container.")
        print(f"Details: {result.stderr}")
        print("\nMake sure you have built the Docker image:")
        print("  cd db/")
        print("  docker build -t blg317e-dev-db .")
        return False

    print("Waiting for database to be ready...")
    time.sleep(5)
    print("Database ready!")
    return True


def stop_database():
    """Stop and remove the database container."""
    print("\nStopping database container...")
    subprocess.run(["docker", "stop", "blg317e-test-db"], capture_output=True)
    subprocess.run(["docker", "rm", "blg317e-test-db"], capture_output=True)
    print("Database container stopped and removed")


async def run_demo():
    db_url = os.environ.get("DATABASE_URL", "postgres://dbuser:insecure-password_NO-NOT-EXPOSE-THIS-DB-TO-PUBLIC@localhost:2345/blg317e")
    pool = await asyncpg.create_pool(db_url)

    async with pool.acquire() as conn:
        for country in TEST_COUNTRIES:
            await conn.execute(
                "INSERT INTO countries (code, name, continent, lat, lng) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (code) DO NOTHING",
                country["code"], country["name"], country.get("continent"),
                country.get("lat"), country.get("lng")
            )

    repo = CountryRepo(pool)
    svc = CountryService(repo)

    countries = await svc.list_countries()
    print(f"\nFound {len(countries)} countries")

    country = await svc.get_country("USA")
    print(f"USA: {country}")

    try:
        await svc.create_country("TUR", "Turkey", "Asia", 38.9637, 35.2433)
        print("Added Turkey successfully")
    except Exception as e:
        print(f"Error adding Turkey: {e}")

    await pool.close()


if __name__ == "__main__":
    if not start_database():
        sys.exit(1)

    try:
        asyncio.run(run_demo())
        print("\n✓ Demo completed successfully!")
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        sys.exit(1)
    finally:
        stop_database()
