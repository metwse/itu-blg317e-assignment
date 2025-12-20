from fixtures import l01_download, l02_misc, l03_economies, l04_worldbank

from src.state import from_env
from src import log

from typing import Optional, Tuple
from dotenv import load_dotenv
import asyncio
import os

STATUS_FILE = ".load_status"

PIPELINE = [
    ('download', l01_download.load),
    ('misc', l02_misc.load),
    ('economies', l03_economies.load),
    ('worldbank', l04_worldbank.load),
    ('end', None)
]


load_dotenv()


def get_last_completed_step() -> Optional[Tuple[str, Optional[str]]]:
    if not os.path.exists(STATUS_FILE):
        return None
    with open(STATUS_FILE, "r") as f:
        step = f.read().strip().split('.')
        return (step[0], step[1] if len(step) > 1 else None)


def save_step_status(step_name, step_part: Optional[str]):
    with open(STATUS_FILE, "w") as f:
        f.write(step_name if step_part is None else f"{step_name}.{step_part}")


async def run_migration(name, func, state):
    log.info(f"Running '{name}'")

    async def run():
        last_step = get_last_completed_step()

        if last_step:
            last_step_name, last_step_part = last_step
        else:
            last_step_name = last_step_part = None

        await func(state,
                   last_step_part if last_step_name == name else None,
                   lambda part: save_step_status(name, part))

        save_step_status(name, None)

    while True:
        try:
            await run()
            log.info(f"Done '{name}'")

            break
        except Exception as err:
            log.error(f"An error occured during '{name}'",
                      err=str(err), ty=type(err))


async def main():
    state = await from_env()

    last_step = get_last_completed_step()
    start_index = 0

    if last_step:
        last_step_name, last_step_part = last_step
        for i, (step_name, _) in enumerate(PIPELINE):
            skip_msg = f"Skipping '{step_name}' as it has already been " \
                       "completed"
            if step_name == last_step_name:
                if last_step_part is None:
                    start_index = i + 1
                    log.info(skip_msg)
                else:
                    start_index = i
                break
            else:
                log.info(skip_msg)

    if start_index == len(PIPELINE) - 1:
        return log.info("All fixtures has already been loaded")

    for name, func in PIPELINE[start_index:-1]:
        await run_migration(name, func, state)

if __name__ == "__main__":
    asyncio.run(main())
