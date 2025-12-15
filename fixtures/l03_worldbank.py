"""
World Bank API Scraper for BLG317E Database Project

This fixture loads data from the World Bank API (https://api.worldbank.org/v2/)
and populates the database with economies and indicator data.

Usage:
    python -m fixtures
"""

import httpx
import asyncio
from typing import Dict, List, Optional, Any
from src.entities import Economy, Region
from src.state import State
from src import log


# World Bank API v2 base URL
BASE_URL = "https://api.worldbank.org/v2"

# Indicator codes matching your entities
HEALTH_INDICATORS = {
    "SH.MED.NUMW.P3": "community_health_workers",
    "SN.ITK.DEFC.ZS": "prevalence_of_undernourishment",
    "SN.ITK.SVFI.ZS": "prevalence_of_severe_food_insecurity",
    "SH.STA.HYGN.ZS": "basic_handwashing_facilities",
    "SH.H2O.SMDW.ZS": "safely_managed_drinking_water_services",
    "SH.STA.DIAB.ZS": "diabetes_prevalence"
}

ECONOMIC_INDICATORS = {
    "NV.IND.TOTL.ZS": "industry",
    "NY.GDP.PCAP.CD": "gdp_per_capita",
    "NE.TRD.GNFS.ZS": "trade",
    "NV.AGR.TOTL.ZS": "agriculture_forestry_and_fishing"
}

ENVIRONMENT_INDICATORS = {
    "EG.USE.PCAP.KG.OE": "energy_use",
    "EG.ELC.ACCS.ZS": "access_to_electricity",
    "EG.USE.COMM.CL.ZS": "alternative_and_nuclear_energy",
    "AG.LND.CROP.ZS": "permanent_cropland",
    "AG.PRD.CROP.XD": "crop_production_index",
    "EG.GDP.PUSE.KO.PP.KD": "gdp_per_unit_of_energy_use"
}

# World Bank region mapping to your Region type
REGION_MAPPING = {
    "EAS": "East Asia & Pacific",
    "ECS": "Europe & Central Asia",
    "LCN": "Latin America & Caribbean",
    "MEA": "Middle East, North Africa, Afghanistan & Pakistan",
    "NAC": "North America",
    "SAS": "South Asia",
    "SSF": "Sub-Saharan Africa",
}


async def fetch_json(client: httpx.AsyncClient, endpoint: str, params: Optional[Dict] = None) -> Optional[List]:
    """Make GET request to World Bank API"""
    url = f"{BASE_URL}/{endpoint}"
    default_params = {
        "format": "json",
        "per_page": 500  # Max allowed
    }
    if params:
        default_params.update(params)

    try:
        response = await client.get(url, params=default_params, timeout=30.0, follow_redirects=True)
        response.raise_for_status()
        data = response.json()

        # World Bank API returns [metadata, data]
        if isinstance(data, list) and len(data) > 1:
            return data[1] if data[1] else None
        return None

    except httpx.HTTPError as e:
        log.error(f"Error fetching {url}: {e}")
        return None


async def get_economies(client: httpx.AsyncClient) -> List[Economy]:
    """
    Fetch all economies (countries) from World Bank API

    Returns list of Economy objects
    """
    log.info("Fetching economies from World Bank API...")
    data = await fetch_json(client, "country")

    if not data:
        return []

    economies = []
    for item in data:
        # Skip aggregates and regions (they don't have capital cities)
        if not item.get("capitalCity"):
            continue

        region_code = item.get("region", {}).get("id", "")
        region_name = REGION_MAPPING.get(region_code)

        # Only include if region is valid
        if region_name:
            economy = Economy(
                code=item["id"],  # 3-letter ISO code
                name=item["name"],
                region=region_name
            )
            economies.append(economy)

    log.info(f"Found {len(economies)} economies")
    return economies


async def get_indicator_data(
    client: httpx.AsyncClient,
    economy_code: str,
    indicator_code: str,
    start_year: int = 2000,
    end_year: int = 2023
) -> Dict[int, Optional[float]]:
    """
    Fetch indicator data for a specific economy

    Returns dict mapping year -> value
    """
    endpoint = f"country/{economy_code}/indicator/{indicator_code}"
    params = {
        "date": f"{start_year}:{end_year}"
    }

    data = await fetch_json(client, endpoint, params)
    if not data:
        return {}

    result = {}
    for item in data:
        try:
            year = int(item.get("date", 0))
            value = item.get("value")
            if year > 0:
                result[year] = float(value) if value is not None else None
        except (ValueError, TypeError):
            continue

    return result


async def scrape_health_indicators(
    client: httpx.AsyncClient,
    state: State,
    economy_codes: List[str],
    years: List[int],
    provider_id: int = 1
):
    """Scrape and load health indicators into database"""
    log.info(f"Scraping health indicators for {len(economy_codes)} economies...")

    total = len(economy_codes)

    for idx, code in enumerate(economy_codes, 1):
        log.info(f"Processing health indicators for {code} ({idx}/{total})...")

        # Get all indicators for this economy
        economy_data = {}
        for indicator_code, field_name in HEALTH_INDICATORS.items():
            data = await get_indicator_data(client, code, indicator_code, min(years), max(years))
            economy_data[field_name] = data
            await asyncio.sleep(0.1)  # Rate limiting

        # Create records for each year
        for year in years:
            from src.entities import HealthIndicator

            indicator = HealthIndicator(
                provider_id=provider_id,
                economy_code=code,
                year=year,
                community_health_workers=economy_data.get("community_health_workers", {}).get(year),
                prevalence_of_undernourishment=economy_data.get("prevalence_of_undernourishment", {}).get(year),
                prevalence_of_severe_food_insecurity=economy_data.get("prevalence_of_severe_food_insecurity", {}).get(year),
                basic_handwashing_facilities=economy_data.get("basic_handwashing_facilities", {}).get(year),
                safely_managed_drinking_water_services=economy_data.get("safely_managed_drinking_water_services", {}).get(year),
                diabetes_prevalence=economy_data.get("diabetes_prevalence", {}).get(year)
            )

            try:
                await state.health_indicator_service.create(indicator)
            except Exception as e:
                # Ignore conflicts (already exists)
                if "duplicate" not in str(e).lower() and "conflict" not in str(e).lower():
                    log.error(f"Error inserting health indicator for {code}/{year}: {e}")


async def scrape_economic_indicators(
    client: httpx.AsyncClient,
    state: State,
    economy_codes: List[str],
    years: List[int],
    provider_id: int = 1
):
    """Scrape and load economic indicators into database"""
    log.info(f"Scraping economic indicators for {len(economy_codes)} economies...")

    total = len(economy_codes)

    for idx, code in enumerate(economy_codes, 1):
        log.info(f"Processing economic indicators for {code} ({idx}/{total})...")

        economy_data = {}
        for indicator_code, field_name in ECONOMIC_INDICATORS.items():
            data = await get_indicator_data(client, code, indicator_code, min(years), max(years))
            economy_data[field_name] = data
            await asyncio.sleep(0.1)

        for year in years:
            from src.entities import EconomicIndicator

            indicator = EconomicIndicator(
                provider_id=provider_id,
                economy_code=code,
                year=year,
                industry=economy_data.get("industry", {}).get(year),
                gdp_per_capita=economy_data.get("gdp_per_capita", {}).get(year),
                trade=economy_data.get("trade", {}).get(year),
                agriculture_forestry_and_fishing=economy_data.get("agriculture_forestry_and_fishing", {}).get(year)
            )

            try:
                await state.economic_indicator_service.create(indicator)
            except Exception as e:
                if "duplicate" not in str(e).lower() and "conflict" not in str(e).lower():
                    log.error(f"Error inserting economic indicator for {code}/{year}: {e}")


async def scrape_environment_indicators(
    client: httpx.AsyncClient,
    state: State,
    economy_codes: List[str],
    years: List[int],
    provider_id: int = 1
):
    """Scrape and load environment indicators into database"""
    log.info(f"Scraping environment indicators for {len(economy_codes)} economies...")

    total = len(economy_codes)

    for idx, code in enumerate(economy_codes, 1):
        log.info(f"Processing environment indicators for {code} ({idx}/{total})...")

        economy_data = {}
        for indicator_code, field_name in ENVIRONMENT_INDICATORS.items():
            data = await get_indicator_data(client, code, indicator_code, min(years), max(years))
            economy_data[field_name] = data
            await asyncio.sleep(0.1)

        for year in years:
            from src.entities import EnvironmentIndicator

            indicator = EnvironmentIndicator(
                provider_id=provider_id,
                economy_code=code,
                year=year,
                energy_use=economy_data.get("energy_use", {}).get(year),
                access_to_electricity=economy_data.get("access_to_electricity", {}).get(year),
                alternative_and_nuclear_energy=economy_data.get("alternative_and_nuclear_energy", {}).get(year),
                permanent_cropland=economy_data.get("permanent_cropland", {}).get(year),
                crop_production_index=economy_data.get("crop_production_index", {}).get(year),
                gdp_per_unit_of_energy_use=economy_data.get("gdp_per_unit_of_energy_use", {}).get(year)
            )

            try:
                await state.environment_indicator_service.create(indicator)
            except Exception as e:
                if "duplicate" not in str(e).lower() and "conflict" not in str(e).lower():
                    log.error(f"Error inserting environment indicator for {code}/{year}: {e}")


async def load(state: State):
    """
    Main fixture loader for World Bank data

    This will:
    1. Fetch and load all economies
    2. Scrape and load health indicators
    3. Scrape and load economic indicators
    4. Scrape and load environment indicators
    """
    async with httpx.AsyncClient() as client:
        # Step 1: Load economies
        log.info("=" * 60)
        log.info("STEP 1: Loading Economies from World Bank")
        log.info("=" * 60)

        economies = await get_economies(client)

        # Track which economies were successfully created or already exist
        valid_economy_codes = []

        for economy in economies:
            try:
                await state.economy_service.create(economy)
                valid_economy_codes.append(economy.code)
                log.info(f"Created economy: {economy.code}")
            except Exception as e:
                # Economy might already exist from l01_economy.load
                if "duplicate" in str(e).lower() or "already exists" in str(e).lower():
                    valid_economy_codes.append(economy.code)
                    log.info(f"Economy {economy.code} already exists, will use it")
                else:
                    log.warning(f"Could not create economy {economy.code}: {e}")

        log.info(f"Loaded {len(valid_economy_codes)} valid economies")

        # Get list of economy codes for scraping - only use valid ones
        # Limit to 10 for testing - remove [:10] for full scrape
        economy_codes = valid_economy_codes[:10]

        # Define years to scrape (last 10 years)
        years = list(range(2014, 2024))

        log.info(f"Will scrape indicators for {len(economy_codes)} economies")
        log.info(f"Years: {years[0]} - {years[-1]}")

        # Step 2: Scrape Health Indicators
        log.info("\n" + "=" * 60)
        log.info("STEP 2: Scraping Health Indicators")
        log.info("=" * 60)
        await scrape_health_indicators(client, state, economy_codes, years)

        # Step 3: Scrape Economic Indicators
        log.info("\n" + "=" * 60)
        log.info("STEP 3: Scraping Economic Indicators")
        log.info("=" * 60)
        await scrape_economic_indicators(client, state, economy_codes, years)

        # Step 4: Scrape Environment Indicators
        log.info("\n" + "=" * 60)
        log.info("STEP 4: Scraping Environment Indicators")
        log.info("=" * 60)
        await scrape_environment_indicators(client, state, economy_codes, years)

        log.info("\n" + "=" * 60)
        log.info("World Bank Data Loading COMPLETE!")
        log.info("=" * 60)
