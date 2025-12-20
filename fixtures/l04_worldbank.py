from fixtures.l01_download import DATA_DIR

from src import log
from src.dto import IndicatorCreateDto
from src.state import State

import csv
import os
from collections import defaultdict


INDICATOR_MAPPING = {
    # health
    'SH.MED.NUMW.P3': 'community_health_workers',
    'SN.ITK.DEFC.ZS': 'prevalence_of_undernourishment',
    'SN.ITK.SVFI.ZS': 'prevalence_of_severe_food_insecurity',
    'SH.STA.HYGN.ZS': 'basic_handwashing_facilities',
    'SH.H2O.SMDW.ZS': 'safely_managed_drinking_water_services',
    'SH.STA.DIAB.ZS': 'diabetes_prevalence',

    # economic
    'NV.IND.TOTL.ZS': 'industry',
    'NY.GDP.PCAP.CD': 'gdp_per_capita',
    'NE.TRD.GNFS.ZS': 'trade',
    'NV.AGR.TOTL.ZS': 'agriculture_forestry_and_fishing',

    # environment
    'EG.USE.PCAP.KG.OE': 'energy_use',
    'EG.ELC.ACCS.ZS': 'access_to_electricity',
    'EG.USE.COMM.CL.ZS': 'alternative_and_nuclear_energy',
    'AG.LND.CROP.ZS': 'permanent_cropland',
    'AG.PRD.CROP.XD': 'crop_production_index',
    'EG.GDP.PUSE.KO.PP.KD': 'gdp_per_unit_of_energy_use'
}


async def load(state: State, *_):
    csv_file_path = os.path.join(DATA_DIR, "WDICSV.csv")

    provider_id = 1

    log.info("Grouping WDI Data in memory...")

    data_buffer = defaultdict(dict)

    with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            indicator_code = row.get('Indicator Code', '')
            country_code = row.get('Country Code', '')

            target_field = INDICATOR_MAPPING.get(indicator_code)
            if not target_field:
                continue

            for year_col, value in row.items():
                if not year_col.isdigit():
                    continue

                if not value:
                    continue

                try:
                    float_val = float(value)
                    year = int(year_col)

                    data_buffer[(country_code, year)][target_field] = float_val
                except ValueError:
                    continue

    log.info("Data grouping complete. "
             f"{len(data_buffer)} records ready to insert.")

    success = 0
    skipped = 0

    for (country_code, year), fields in data_buffer.items():
        try:
            dto = IndicatorCreateDto(
                provider_id=provider_id,
                economy_code=country_code,
                year=year,
                **fields
            )

            await state.indicator_service.create(dto)
            success += 1

            if success % 1000 == 0:
                log.info(f"Inserted {success} indicators...")

        except Exception as e:
            log.error(f"Skipping {country_code}-{year}: {e}")
            skipped += 1

    log.info(f"Load Complete. Inserted: {success}, Skipped/Error: {skipped}")
