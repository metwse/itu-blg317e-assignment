import asyncio

try:
    from service.country_service import CountryService
    from repo.mock_country_repo import MockCountryRepo
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))
    from service.country_service import CountryService
    from repo.mock_country_repo import MockCountryRepo


async def run_demo():
    repo = MockCountryRepo()
    svc = CountryService(repo)
    await svc.create_country("us", "United States")
    await svc.list_countries()
    await svc.get_country("US")
    try:
        await svc.create_country("US", "United States Duplicate")
    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(run_demo())
