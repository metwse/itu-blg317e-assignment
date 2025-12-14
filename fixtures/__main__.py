from fixtures import l01_economy

from src.state import from_env

from dotenv import load_dotenv
import asyncio


load_dotenv()


async def main():
    state = await from_env()

    await l01_economy.load(state.economy_service)


if __name__ == "__main__":
    asyncio.run(main())
