from fixtures.l01_download import ECONOMIES_FILE_PATH

from src.dto import EconomyCreateDto
from src.state import State

import json


async def load(state: State, *_):
    with open(ECONOMIES_FILE_PATH, mode='r', encoding='utf-8') as f:
        content = f.read()
        data = json.loads(content)[1]

    success = 0
    skipped = 0

    for item in data:
        try:
            region_info = item.get('region', {})
            income_info = item.get('incomeLevel', {})

            region_id = region_info.get('id', '')
            region_val = region_info.get('value', '')
            income_id = income_info.get('id', '')

            is_aggregate = (region_val == 'Aggregates') or (region_id == 'NA')

            final_region = region_id \
                if (not is_aggregate and region_id != 'NA') else None

            final_income = income_id \
                if (not is_aggregate and income_id != 'NA') else None

            try:
                lat_val = float(item['latitude']) \
                    if item.get('latitude') else None
                lng_val = float(item['longitude']) \
                    if item.get('longitude') else None
            except ValueError:
                lat_val, lng_val = None, None

            await state.economy_service.create(
                EconomyCreateDto(
                    code=item['id'],
                    name=item['name'],
                    region=final_region,
                    income_level=final_income,
                    is_aggregate=is_aggregate,
                    capital_city=item.get('capitalCity'),
                    lat=lat_val,
                    lng=lng_val
                ))
            success += 1

        except Exception as e:
            print(f"Skipping {item.get('id', 'unknown')}: {e}")
            skipped += 1

    print(f"Load Complete. Inserted: {success}, Skipped/Error: {skipped}")
