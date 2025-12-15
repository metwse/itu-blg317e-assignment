# World Bank API Scraper

Comprehensive scraper for the World Bank Data API v2 to populate the BLG317E database project.

## Overview

This scraper fetches data from the World Bank's public API and generates:
- Economy (country) data with 3-letter ISO codes and World Bank regions
- Health indicators data
- Economic indicators data
- Environment indicators data

All data is exported in both JSON and SQL INSERT statement formats.

## World Bank API Documentation

**Base URL:** `https://api.worldbank.org/v2`

**Format:** JSON (default parameter: `format=json`)

### Key API Endpoints

1. **Countries/Economies**
   ```
   GET /v2/country?format=json&per_page=500
   ```
   Returns all countries with metadata including region, income level, capital city.

2. **Indicators**
   ```
   GET /v2/country/{country_code}/indicator/{indicator_code}?format=json&date={start}:{end}
   ```
   Returns time series data for a specific indicator and country.

3. **All Indicators List**
   ```
   GET /v2/indicator?format=json&per_page=500
   ```
   Returns list of all available indicators.

## Indicator Mappings

### Health Indicators
| World Bank Code | Database Field | Description |
|----------------|----------------|-------------|
| SH.MED.NUMW.P3 | community_health_workers | Community health workers (per 1,000 people) |
| SN.ITK.DEFC.ZS | prevalence_of_undernourishment | Prevalence of undernourishment (% of population) |
| SN.ITK.SVFI.ZS | prevalence_of_severe_food_insecurity | Prevalence of severe food insecurity |
| SH.STA.HYGN.ZS | basic_handwashing_facilities | People with basic handwashing facilities (%) |
| SH.H2O.SMDW.ZS | safely_managed_drinking_water_services | Safely managed drinking water services (%) |
| SH.STA.DIAB.ZS | diabetes_prevalence | Diabetes prevalence (% of population ages 20-79) |

### Economic Indicators
| World Bank Code | Database Field | Description |
|----------------|----------------|-------------|
| NV.IND.TOTL.ZS | industry | Industry (including construction), value added (% of GDP) |
| NY.GDP.PCAP.CD | gdp_per_capita | GDP per capita (current US$) |
| NE.TRD.GNFS.ZS | trade | Trade (% of GDP) |
| NV.AGR.TOTL.ZS | agriculture_forestry_and_fishing | Agriculture, forestry, fishing (% of GDP) |

### Environment Indicators
| World Bank Code | Database Field | Description |
|----------------|----------------|-------------|
| EG.USE.PCAP.KG.OE | energy_use | Energy use (kg of oil equivalent per capita) |
| EG.ELC.ACCS.ZS | access_to_electricity | Access to electricity (% of population) |
| EG.USE.COMM.CL.ZS | alternative_and_nuclear_energy | Alternative and nuclear energy (% of total energy use) |
| AG.LND.CROP.ZS | permanent_cropland | Permanent cropland (% of land area) |
| AG.PRD.CROP.XD | crop_production_index | Crop production index (2014-2016 = 100) |
| EG.GDP.PUSE.KO.PP.KD | gdp_per_unit_of_energy_use | GDP per unit of energy use (constant 2021 PPP $ per kg of oil equivalent) |

## Region Mapping

World Bank regions mapped to database Region type:

```python
EAS → "East Asia & Pacific"
ECS → "Europe & Central Asia"
LCN → "Latin America & Caribbean"
MEA → "Middle East, North Africa, Afghanistan & Pakistan"
NAC → "North America"
SAS → "South Asia"
SSF → "Sub-Saharan Africa"
```

## Usage

### Basic Usage

```powershell
# Run the scraper
python scripts/worldbank_scraper.py
```

This will:
1. Fetch all economies from World Bank API
2. Scrape health, economic, and environment indicators
3. Generate JSON and SQL files in the `output/` directory

### Output Files

The scraper generates the following files in `output/`:

- `economies.json` - Economy data in JSON format
- `economies.sql` - SQL INSERT statements for economies table
- `health_indicators.json` - Health indicator data in JSON
- `health_indicators.sql` - SQL INSERT statements for health_indicators table
- `economic_indicators.json` - Economic indicator data in JSON
- `economic_indicators.sql` - SQL INSERT statements for economic_indicators table
- `environment_indicators.json` - Environment indicator data in JSON
- `environment_indicators.sql` - SQL INSERT statements for environment_indicators table

### Customization

Edit `worldbank_scraper.py` to customize:

**Limit economies** (line ~400):
```python
# Scrape only first 10 economies for testing
economy_codes = [e["code"] for e in economies[:10]]

# Or scrape all economies
economy_codes = [e["code"] for e in economies]
```

**Year range** (line ~406):
```python
# Last 10 years
years = list(range(2014, 2024))

# Or specific years
years = [2015, 2016, 2017, 2018, 2019, 2020]

# Or full range
years = list(range(1960, 2024))
```

## Database Integration

### Loading Data into Database

**Option 1: Use SQL files directly**

```sql
-- Load economies
\i output/economies.sql

-- Load indicators (requires provider_id)
-- Note: Indicator tables need provider_id which must be set manually
-- or the SQL files need to be edited to include provider_id
```

**Option 2: Use Python API**

```python
import requests
import json

# Load economies
with open('output/economies.json') as f:
    economies = json.load(f)

for economy in economies:
    requests.post(
        'http://localhost:5000/internal/economies/',
        headers={'token': 'your-admin-token'},
        json=economy
    )

# Load health indicators
with open('output/health_indicators.json') as f:
    indicators = json.load(f)

for indicator in indicators:
    # Add provider_id
    indicator['provider_id'] = 1
    requests.post(
        'http://localhost:5000/internal/health_indicators/',
        headers={'token': 'your-admin-token'},
        json=indicator
    )
```

## API Rate Limiting

The scraper includes built-in rate limiting:
- 0.2 second delay between requests
- 30 second timeout per request
- 500 items per page (maximum allowed by World Bank API)

For large-scale scraping, the complete operation may take several hours.

## Additional World Bank Indicators

You can add more indicators by updating the dictionaries at the top of `worldbank_scraper.py`:

**Popular indicators:**
- `SP.POP.TOTL` - Population, total
- `SP.DYN.LE00.IN` - Life expectancy at birth
- `SE.XPD.TOTL.GD.ZS` - Government expenditure on education (% of GDP)
- `SH.XPD.CHEX.GD.ZS` - Current health expenditure (% of GDP)
- `EN.ATM.CO2E.PC` - CO2 emissions (metric tons per capita)
- `NY.GDP.MKTP.KD.ZG` - GDP growth (annual %)

Browse all indicators: https://data.worldbank.org/indicator

## Troubleshooting

**Missing data:**
- Not all indicators have data for all countries and years
- The scraper stores `NULL` for missing values
- Check the World Bank website to verify data availability

**Connection errors:**
- World Bank API may be temporarily unavailable
- The scraper will retry automatically
- Check your internet connection

**Large dataset:**
- For all countries and full year range, expect several GB of data
- Use the year range and country filters for testing
- Consider scraping incrementally (by year or country groups)

## API Response Format

World Bank API returns data in this format:

```json
[
  {
    "page": 1,
    "pages": 1,
    "per_page": 500,
    "total": 296
  },
  [
    {
      "id": "ABW",
      "iso2Code": "AW",
      "name": "Aruba",
      "region": {
        "id": "LCN",
        "value": "Latin America & Caribbean"
      },
      "capitalCity": "Oranjestad",
      "longitude": "-70.0167",
      "latitude": "12.5167"
    }
  ]
]
```

The scraper parses this format automatically.

## References

- [World Bank Data API Documentation](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information)
- [World Bank Open Data](https://data.worldbank.org/)
- [Indicator API Documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)
