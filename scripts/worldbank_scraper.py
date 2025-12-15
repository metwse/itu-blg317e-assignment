"""
World Bank API Scraper for BLG317E Database Project

This script scrapes data from the World Bank API (https://api.worldbank.org/v2/)
and populates the database with economies, and indicator data.

Usage:
    python scripts/worldbank_scraper.py
"""

import requests
import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

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
    "": None  # For aggregates/world
}


class WorldBankScraper:
    """Scraper for World Bank Data API v2"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make GET request to World Bank API"""
        url = f"{BASE_URL}/{endpoint}"
        default_params = {
            "format": "json",
            "per_page": 500  # Max allowed
        }
        if params:
            default_params.update(params)

        try:
            response = self.session.get(url, params=default_params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # World Bank API returns [metadata, data]
            if isinstance(data, list) and len(data) > 1:
                return data[1] if data[1] else None
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_economies(self) -> List[Dict[str, Any]]:
        """
        Fetch all economies (countries) from World Bank API

        Returns list of economies with structure:
        {
            'code': 'USA',
            'name': 'United States',
            'region': 'North America'
        }
        """
        print("Fetching economies...")
        data = self._get("country")

        if not data:
            return []

        economies = []
        for item in data:
            # Skip aggregates and regions
            if item.get("capitalCity") == "":
                continue

            region_code = item.get("region", {}).get("id", "")
            region = REGION_MAPPING.get(region_code, None)

            economy = {
                "code": item["id"],  # 3-letter ISO code
                "name": item["name"],
                "region": region
            }
            economies.append(economy)

        print(f"Found {len(economies)} economies")
        return economies

    def get_indicator_data(
        self,
        economy_code: str,
        indicator_code: str,
        start_year: int = 1960,
        end_year: int = 2024
    ) -> Dict[int, Optional[float]]:
        """
        Fetch indicator data for a specific economy

        Returns dict mapping year -> value
        """
        endpoint = f"country/{economy_code}/indicator/{indicator_code}"
        params = {
            "date": f"{start_year}:{end_year}"
        }

        data = self._get(endpoint, params)
        if not data:
            return {}

        result = {}
        for item in data:
            year = int(item.get("date", 0))
            value = item.get("value")
            if year > 0:
                result[year] = float(value) if value is not None else None

        return result

    def scrape_health_indicators(
        self,
        economy_codes: List[str],
        years: List[int]
    ) -> List[Dict]:
        """Scrape health indicators for specified economies and years"""
        print(f"\nScraping health indicators for {len(economy_codes)} economies...")

        results = []
        total = len(economy_codes)

        for idx, code in enumerate(economy_codes, 1):
            print(f"Processing {code} ({idx}/{total})...", end="\r")

            # Get all indicators for this economy
            economy_data = {}
            for indicator_code, field_name in HEALTH_INDICATORS.items():
                data = self.get_indicator_data(code, indicator_code)
                economy_data[field_name] = data
                time.sleep(0.2)  # Rate limiting

            # Create records for each year
            for year in years:
                record = {
                    "economy_code": code,
                    "year": year
                }

                for field_name in HEALTH_INDICATORS.values():
                    record[field_name] = economy_data.get(field_name, {}).get(year)

                results.append(record)

        print(f"\nCollected {len(results)} health indicator records")
        return results

    def scrape_economic_indicators(
        self,
        economy_codes: List[str],
        years: List[int]
    ) -> List[Dict]:
        """Scrape economic indicators for specified economies and years"""
        print(f"\nScraping economic indicators for {len(economy_codes)} economies...")

        results = []
        total = len(economy_codes)

        for idx, code in enumerate(economy_codes, 1):
            print(f"Processing {code} ({idx}/{total})...", end="\r")

            economy_data = {}
            for indicator_code, field_name in ECONOMIC_INDICATORS.items():
                data = self.get_indicator_data(code, indicator_code)
                economy_data[field_name] = data
                time.sleep(0.2)

            for year in years:
                record = {
                    "economy_code": code,
                    "year": year
                }

                for field_name in ECONOMIC_INDICATORS.values():
                    record[field_name] = economy_data.get(field_name, {}).get(year)

                results.append(record)

        print(f"\nCollected {len(results)} economic indicator records")
        return results

    def scrape_environment_indicators(
        self,
        economy_codes: List[str],
        years: List[int]
    ) -> List[Dict]:
        """Scrape environment indicators for specified economies and years"""
        print(f"\nScraping environment indicators for {len(economy_codes)} economies...")

        results = []
        total = len(economy_codes)

        for idx, code in enumerate(economy_codes, 1):
            print(f"Processing {code} ({idx}/{total})...", end="\r")

            economy_data = {}
            for indicator_code, field_name in ENVIRONMENT_INDICATORS.items():
                data = self.get_indicator_data(code, indicator_code)
                economy_data[field_name] = data
                time.sleep(0.2)

            for year in years:
                record = {
                    "economy_code": code,
                    "year": year
                }

                for field_name in ENVIRONMENT_INDICATORS.values():
                    record[field_name] = economy_data.get(field_name, {}).get(year)

                results.append(record)

        print(f"\nCollected {len(results)} environment indicator records")
        return results

    def save_to_json(self, data: Any, filename: str):
        """Save data to JSON file"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved to {filepath}")

    def generate_sql_inserts(self, table: str, records: List[Dict]) -> List[str]:
        """Generate SQL INSERT statements"""
        if not records:
            return []

        statements = []
        fields = list(records[0].keys())

        for record in records:
            values = []
            for field in fields:
                value = record[field]
                if value is None:
                    values.append("NULL")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    # Escape single quotes
                    escaped = str(value).replace("'", "''")
                    values.append(f"'{escaped}'")

            sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(values)});"
            statements.append(sql)

        return statements

    def save_sql_inserts(self, table: str, records: List[Dict], filename: str):
        """Save SQL INSERT statements to file"""
        statements = self.generate_sql_inserts(table, records)
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"-- Generated on {datetime.now().isoformat()}\n")
            f.write(f"-- Table: {table}\n")
            f.write(f"-- Records: {len(statements)}\n\n")
            for stmt in statements:
                f.write(stmt + "\n")

        print(f"Saved {len(statements)} SQL statements to {filepath}")


def main():
    """Main execution function"""
    scraper = WorldBankScraper()

    # 1. Get all economies
    print("=" * 60)
    print("STEP 1: Fetching Economies")
    print("=" * 60)
    economies = scraper.get_economies()
    scraper.save_to_json(economies, "economies.json")
    scraper.save_sql_inserts("economies", economies, "economies.sql")

    # Get list of economy codes (limit to first 10 for testing, remove limit for full scrape)
    economy_codes = [e["code"] for e in economies[:10]]  # Remove [:10] for all economies
    print(f"\nWill scrape data for {len(economy_codes)} economies")

    # Define years to scrape (last 10 years for testing)
    years = list(range(2014, 2024))  # Adjust range as needed
    print(f"Years to scrape: {years[0]} - {years[-1]}")

    # 2. Scrape Health Indicators
    print("\n" + "=" * 60)
    print("STEP 2: Scraping Health Indicators")
    print("=" * 60)
    health_data = scraper.scrape_health_indicators(economy_codes, years)
    scraper.save_to_json(health_data, "health_indicators.json")
    scraper.save_sql_inserts("health_indicators", health_data, "health_indicators.sql")

    # 3. Scrape Economic Indicators
    print("\n" + "=" * 60)
    print("STEP 3: Scraping Economic Indicators")
    print("=" * 60)
    economic_data = scraper.scrape_economic_indicators(economy_codes, years)
    scraper.save_to_json(economic_data, "economic_indicators.json")
    scraper.save_sql_inserts("economic_indicators", economic_data, "economic_indicators.sql")

    # 4. Scrape Environment Indicators
    print("\n" + "=" * 60)
    print("STEP 4: Scraping Environment Indicators")
    print("=" * 60)
    environment_data = scraper.scrape_environment_indicators(economy_codes, years)
    scraper.save_to_json(environment_data, "environment_indicators.json")
    scraper.save_sql_inserts("environment_indicators", environment_data, "environment_indicators.sql")

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE!")
    print("=" * 60)
    print(f"Total economies: {len(economies)}")
    print(f"Health records: {len(health_data)}")
    print(f"Economic records: {len(economic_data)}")
    print(f"Environment records: {len(environment_data)}")
    print(f"\nAll files saved to: {scraper.output_dir.absolute()}")


if __name__ == "__main__":
    main()
