from src import log

import asyncio
import shutil
import os
import urllib.request
import zipfile


ZIP_URL = \
    "https://databank.worldbank.org/data/download/WDI_CSV.zip"
ECONOMIES_URL = \
    "https://api.worldbank.org/v2/countries?format=json&per_page=500"

TEMP_DIR = ".tmp"
ZIP_FILE_PATH = os.path.join(TEMP_DIR, "WDI_CSV.zip")
ECONOMIES_FILE_PATH = os.path.join(TEMP_DIR, "economies.json")
DATA_DIR = os.path.join(TEMP_DIR, "data")


def download_and_extract(last_step, set_step):
    while True:
        match last_step:
            case None:
                if os.path.exists(TEMP_DIR):
                    log.info(f"Cleaned directory: {TEMP_DIR}")
                    shutil.rmtree(TEMP_DIR)
                os.makedirs(TEMP_DIR)

                log.info(f"Downloading from {ZIP_URL}...")

                try:
                    urllib.request.urlretrieve(ZIP_URL, ZIP_FILE_PATH)
                    log.info("Download completed.")
                except Exception as e:
                    log.error(f"Error during download: {e}")
                    return

                set_step("downloaded_zip")
                last_step = "downloaded_zip"
            case "downloaded_zip":
                log.info("Extracting files...")
                if os.path.exists(DATA_DIR):
                    shutil.rmtree(DATA_DIR)
                    log.info(f"Cleaned directory: {DATA_DIR}")

                try:
                    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
                        zip_ref.extractall(DATA_DIR)
                    log.info(f"Extraction completed to: {DATA_DIR}")
                except Exception as e:
                    log.error(f"Error during extraction: {e}")

                set_step("extracted_zip")
                last_step = "extracted_zip"
            case "extracted_zip":
                log.info(f"Downloading from {ECONOMIES_URL}...")

                try:
                    urllib.request.urlretrieve(ECONOMIES_URL,
                                               ECONOMIES_FILE_PATH)
                    log.info("Download completed.")
                except Exception as e:
                    log.error(f"Error during download: {e}")
                    return

                break


async def load(_, last_step, set_step):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, download_and_extract, last_step, set_step)
