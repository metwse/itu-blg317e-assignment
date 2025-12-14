from fixtures import l01_economy

from src.state import from_env
from src import log

from dotenv import load_dotenv
import asyncio
import os

STATUS_FILE = ".load_status"

load_dotenv()


def get_last_completed_step():
    if not os.path.exists(STATUS_FILE):
        return None
    with open(STATUS_FILE, "r") as f:
        return f.read().strip()


def save_step_status(step_name):
    with open(STATUS_FILE, "w") as f:
        f.write(step_name)


pipeline = [
    ("economies", l01_economy.load)
]


async def main():
    state = await from_env()

    last_step = get_last_completed_step()
    start_index = 0

    if last_step:
        for i, (name, _) in enumerate(pipeline):
            if name == last_step:
                start_index = i + 1
                log.info(f"Skipping '{name}' as it has already been completed")
                break

    for name, func in pipeline[start_index:]:
        log.info(f"Running '{name}'")
        try:
            await func(state)

            save_step_status(name)
            log.info(f"Done '{name}'")
        except Exception as e:
            log.error(f"An error occured during '{name}'", e=str(e))

    if start_index >= len(pipeline):
        log.info("All fixtures has already been loaded")


if __name__ == "__main__":
    asyncio.run(main())
