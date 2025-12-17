-- "indicators" table
-- -------------------------------------------------------------
CREATE TABLE indicators (
    -- Composite Primary Key
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    economy_code char(3) NOT NULL REFERENCES economies (code) ON DELETE CASCADE,
    year integer NOT NULL,

    -- Economic Indicators
    industry real,
    gdp_per_capita real,
    trade real,
    agriculture_forestry_and_fishing real,

    -- Health Indicators
    community_health_workers real,
    prevalence_of_undernourishment real,
    prevalence_of_severe_food_insecurity real,
    basic_handwashing_facilities real,
    safely_managed_drinking_water_services real,
    diabetes_prevalence real,

    -- Environment Indicators
    energy_use real,
    access_to_electricity real,
    alternative_and_nuclear_energy real,
    permanent_cropland real,
    crop_production_index real,
    gdp_per_unit_of_energy_use real,

    -- Constraint
    PRIMARY KEY (provider_id, economy_code, year)
);

-- 1 "economic_indicators" view
-- -------------------------------------------------------------
CREATE VIEW economic_indicators AS
    SELECT
        provider_id,
        economy_code,
        year,
        industry,
        gdp_per_capita,
        trade,
        agriculture_forestry_and_fishing
    FROM indicators;

-- 2 "health_indicators" view
-- -------------------------------------------------------------
CREATE VIEW health_indicators AS
    SELECT
        provider_id,
        economy_code,
        year,
        community_health_workers,
        prevalence_of_undernourishment,
        prevalence_of_severe_food_insecurity,
        basic_handwashing_facilities,
        safely_managed_drinking_water_services,
        diabetes_prevalence
    FROM indicators;

-- 3 "environment_indicators" view
-- -------------------------------------------------------------
CREATE VIEW environment_indicators AS
    SELECT
        provider_id,
        economy_code,
        year,
        energy_use,
        access_to_electricity,
        alternative_and_nuclear_energy,
        permanent_cropland,
        crop_production_index,
        gdp_per_unit_of_energy_use
    FROM indicators;
