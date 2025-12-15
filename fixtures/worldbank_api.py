from src import log

import httpx
from typing import Dict, List, Optional

BASE_URL = "https://api.worldbank.org/v2"

HEALTH_INDICATORS = {
    'SH.MED.NUMW.P3': 'community_health_workers',
    'SN.ITK.DEFC.ZS': 'prevalence_of_undernourishment',
    'SN.ITK.SVFI.ZS': 'prevalence_of_severe_food_insecurity',
    'SH.STA.HYGN.ZS': 'basic_handwashing_facilities',
    'SH.H2O.SMDW.ZS': 'safely_managed_drinking_water_services',
    'SH.STA.DIAB.ZS': 'diabetes_prevalence'
}

ECONOMIC_INDICATORS = {
    'NV.IND.TOTL.ZS': 'industry',
    'NY.GDP.PCAP.CD': 'gdp_per_capita',
    'NE.TRD.GNFS.ZS': 'trade',
    'NV.AGR.TOTL.ZS': 'agriculture_forestry_and_fishing'
}

ENVIRONMENT_INDICATORS = {
    'EG.USE.PCAP.KG.OE': 'energy_use',
    'EG.ELC.ACCS.ZS': 'access_to_electricity',
    'EG.USE.COMM.CL.ZS': 'alternative_and_nuclear_energy',
    'AG.LND.CROP.ZS': 'permanent_cropland',
    'AG.PRD.CROP.XD': 'crop_production_index',
    'EG.GDP.PUSE.KO.PP.KD': 'gdp_per_unit_of_energy_use'
}

# World Bank region mapping to Region type
REGION_MAPPING = {
    'EAS': "East Asia & Pacific",
    'ECS': "Europe & Central Asia",
    'LCN': "Latin America & Caribbean",
    'MEA': "Middle East, North Africa, Afghanistan & Pakistan",
    'NAC': "North America",
    'SAS': "South Asia",
    'SSF': "Sub-Saharan Africa",
}


async def fetch(endpoint: str,
                all=True,
                params: Optional[Dict] = None) -> List:
    """Fetch all items in pagitated """

    url = f"{BASE_URL}/{endpoint}"
    log.info(f"Fetching {url}...")

    default_params = {
        'format': "json",
        'per_page': 500  # Max allowed
    }

    if params:
        default_params.update(params)

    page = 1
    res = []

    client = httpx.AsyncClient()
    while True:
        response = await client.get(url,
                                    params={
                                        'page': page,
                                        **default_params
                                    },
                                    timeout=30.0,
                                    follow_redirects=True)
        response.raise_for_status()
        [page_info, data] = response.json()

        res.extend(data)
        page += 1

        if page > page_info['pages'] or not all:
            break

    return res


async def fetch_indicators(indicator_mapping: Dict[str, str],
                           economies: List[str]):
    res = {}

    for economy in economies:
        log.info(f"Fetching all indicators for {economy}...")
        res[economy] = {}
        for wb_indicator, indicator in indicator_mapping.items():
            res[economy][indicator] = \
                await fetch(f"country/{economy}/indicator/{wb_indicator}",
                            all=False, params={'per_page': 50})

    return res
