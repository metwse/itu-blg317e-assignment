# Public API `/api/public`
This API provides read-only access to the indicator database. It is designed
for public consumption and does **not require authentication**. All endpoints
return data with resolved foreign key relationships (JOINs) for ease of use.


## Resources
### Economies
Browse world economies with their geographic and classification metadata.

#### List All Economies
Returns all economies joined with their region and income level names.

* **Endpoint:** `GET /economies`
* **Response:**
```json
[
  {
    "code": "TUR",
    "name": "Türkiye",
    "is_aggregate": false,
    "capital_city": "Ankara",
    "lat": 39.9334,
    "lng": 32.8597,
    "region_code": "ECS",
    "region_name": "Europe & Central Asia",
    "income_level_code": "UMC",
    "income_level_name": "Upper middle income"
  },
  ...
]
```


### Regions
Lookup table for geographic regions.

#### List All Regions
* **Endpoint:** `GET /regions`
* **Response:**
```json
[
  { "id": "ECS", "name": "Europe & Central Asia" },
  { "id": "NAC", "name": "North America" },
  ...
]
```


### Income Levels
Lookup table for World Bank income classifications.

#### List All Income Levels
* **Endpoint:** `GET /income-levels`
* **Response:**
```json
[
  { "id": "HIC", "name": "High income" },
  { "id": "UMC", "name": "Upper middle income" },
  ...
]
```


### Providers
Data source institutions joined with their admin/technical user names.

#### List All Providers
* **Endpoint:** `GET /providers`
* **Response:**
```json
[
  {
    "id": 10,
    "name": "Turkey Statistics Agency",
    "description": "Official data provider for TUR",
    "website_url": "https://turkstat.gov.tr",
    "admin_name": "Metehan Selvi",
    "tech_name": "John Doe"
  },
  ...
]
```


### Indicators
The core data resource. All indicator endpoints return data joined with
economy, provider, region, and income level information.

#### List All Indicators
Returns paginated indicator data with full join resolution.

* **Endpoint:** `GET /indicators`
* **Query Parameters:**
  * `economy_code` - Filter by economy (e.g., `TUR`)
  * `region` - Filter by region code (e.g., `ECS`)
  * `year` - Filter by exact year
  * `year_start` - Filter by year range start
  * `year_end` - Filter by year range end
  * `provider_id` - Filter by provider ID
  * `limit` - Max results (default: 100)
  * `offset` - Pagination offset (default: 0)

* **Response:**
```json
[
  {
    "provider_id": 10,
    "provider_name": "Turkey Statistics Agency",
    "economy_code": "TUR",
    "economy_name": "Türkiye",
    "region_name": "Europe & Central Asia",
    "income_level": "Upper middle income",
    "year": 2023,
    "gdp_per_capita": 12000.50,
    "industry": 32.5,
    "trade": 65.2,
    "agriculture_forestry_and_fishing": 6.8,
    "community_health_workers": 2.1,
    "diabetes_prevalence": 5.4,
    "prevalence_of_undernourishment": null,
    "prevalence_of_severe_food_insecurity": null,
    "basic_handwashing_facilities": 95.0,
    "safely_managed_drinking_water_services": 98.5,
    "access_to_electricity": 100.0,
    "energy_use": 500.2,
    "alternative_and_nuclear_energy": 12.3,
    "permanent_cropland": 4.5,
    "crop_production_index": 105.2,
    "gdp_per_unit_of_energy_use": 8.5
  },
  ...
]
```


#### List Economic Indicators
Returns only economic-related fields (GDP, industry, trade, agriculture).

* **Endpoint:** `GET /indicators/economic`
* **Query Parameters:**
  * `limit` - Max results (default: 100)
  * `offset` - Pagination offset

* **Response:**
```json
[
  {
    "economy_code": "TUR",
    "economy_name": "Türkiye",
    "region_name": "Europe & Central Asia",
    "year": 2023,
    "gdp_per_capita": 12000.50,
    "industry": 32.5,
    "trade": 65.2,
    "agriculture_forestry_and_fishing": 6.8,
    "provider_name": "Turkey Statistics Agency"
  },
  ...
]
```


#### List Health Indicators
Returns only health-related fields.

* **Endpoint:** `GET /indicators/health`
* **Query Parameters:**
  * `limit` - Max results (default: 100)
  * `offset` - Pagination offset

* **Response:**
```json
[
  {
    "economy_code": "TUR",
    "economy_name": "Türkiye",
    "region_name": "Europe & Central Asia",
    "year": 2023,
    "community_health_workers": 2.1,
    "diabetes_prevalence": 5.4,
    "prevalence_of_undernourishment": 2.5,
    "prevalence_of_severe_food_insecurity": 1.2,
    "basic_handwashing_facilities": 95.0,
    "safely_managed_drinking_water_services": 98.5,
    "provider_name": "Turkey Statistics Agency"
  },
  ...
]
```


#### List Environment Indicators
Returns only environment-related fields.

* **Endpoint:** `GET /indicators/environment`
* **Query Parameters:**
  * `limit` - Max results (default: 100)
  * `offset` - Pagination offset

* **Response:**
```json
[
  {
    "economy_code": "TUR",
    "economy_name": "Türkiye",
    "region_name": "Europe & Central Asia",
    "year": 2023,
    "access_to_electricity": 100.0,
    "energy_use": 500.2,
    "alternative_and_nuclear_energy": 12.3,
    "permanent_cropland": 4.5,
    "crop_production_index": 105.2,
    "gdp_per_unit_of_energy_use": 8.5,
    "provider_name": "Turkey Statistics Agency"
  },
  ...
]
```


### Statistics
Aggregate database statistics.

#### Get Database Stats
Returns counts and ranges for the database.

* **Endpoint:** `GET /stats`
* **Response:**
```json
{
  "economies": 265,
  "providers": 12,
  "indicators": 15420,
  "year_range": {
    "min_year": 1990,
    "max_year": 2023
  }
}
```
