from src import log
from src.dto import ProviderCreateDto, UserCreateDto
from src.state import State


async def load(state: State, *_):
    clean = input("Do you want to truncate all tables for clean loading? "
                  "(Y/n): ")

    if clean == 'Y':
        for field in state.__dataclass_fields__:
            if field.endswith("service"):
                print(f"Truncating {field}...")
                await getattr(state, field).truncate_cascade()
    else:
        print("!!! Skip truncate")

    try:
        await state.user_service.create(
            UserCreateDto(
                email="wb-admin@example.com",
                password="admin",
                name="WorldBank Admin"
            ))

        await state.user_service.create(
            UserCreateDto(
                email="wb-technical@example.com",
                password="technical",
                name="WorldBank Technical"
            ))

        await state.provider_service.create(
            ProviderCreateDto(
                administrative_account=1,
                technical_account=2,
                name="WorldBank",
                website_url="https://worldbank.org/",
                description="The World Bank is an international bank that "
                            "lends money and other help to developing "
                            "nations for infrastructure. The World Bank has "
                            "the goal of reducing poverty.\n\n"
                            "The World Bank is part of the World Bank Group",
                immutable=False
            ))
    except Exception as e:
        log.error(f"Skipping provider creation: {e}")
