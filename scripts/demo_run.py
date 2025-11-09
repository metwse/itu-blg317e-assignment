import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.test_data import TEST_COUNTRIES  # noqa: E402
from src.service.country_service import CountryService  # noqa: E402
from src.repo.in_memory_repo import InMemoryRepo  # noqa: E402


async def run_demo():
    # Use in-memory repository (no database required)
    repo = InMemoryRepo()
    svc = CountryService(repo)

    # Load test data
    print("Loading test data...")
    for country in TEST_COUNTRIES:
        await repo.insert_country(
            country["code"], country["name"], country.get("continent"),
            country.get("lat"), country.get("lng")
        )

    # Test operations
    countries = await svc.list_countries()
    print(f"Found {len(countries)} countries")

    country = await svc.get_country("USA")
    print(f"USA: {country}")

    # Try to add a new country
    try:
        await svc.create_country("TUR", "Turkey", "Asia", 38.9637, 35.2433)
        print("Added Turkey successfully")
    except Exception as e:
        print(f"Error adding Turkey: {e}")

    # Show final count
    countries = await svc.list_countries()
    print(f"Total countries: {len(countries)}")


if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
        print("\n✓ Demo completed successfully!")
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        sys.exit(1)
