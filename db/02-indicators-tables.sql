-- 1 "economic_indicators" table
-- -------------------------------------------------------------
CREATE TABLE economic_indicators (
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    country_code char(3) NOT NULL REFERENCES countries (code) ON DELETE CASCADE,
    year integer NOT NULL,
    -- % of GDP
    industry real,
    -- US$
    gdp_per_capita real,
    -- % of GDP
    trade real,
    -- % of GDP
    agriculture_forestry_and_fishing real
);

-- 2 "health_indicators" table
-- -------------------------------------------------------------
CREATE TABLE health_indicators (
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    country_code char(3) NOT NULL REFERENCES countries (code) ON DELETE CASCADE,
    year integer NOT NULL,
    -- per 1,000 people
    community_health_workers integer,
    -- % of population
    prevalence_of_undernourishment real,
    -- % of population
    prevalence_of_severe_food_insecurity real,
    -- % of population
    basic_handwashing_facilities real,
    -- % of population
    safely_managed_drinking_water_services real,
    -- % of population
    diabetes_prevalence real
);

-- 3 "environment_indicators" table
-- -------------------------------------------------------------
CREATE TABLE environment_indicators (
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    country_code char(3) NOT NULL REFERENCES countries (code) ON DELETE CASCADE,
    year integer NOT NULL,
    -- kg of oil equivalent per capita
    energy_use real,
    -- % of population
    access_to_electricity real,
    -- % of total energy use
    alternative_and_nuclear_energy real,
    -- % of land area
    permanent_cropland real,
    -- 2014-2016 = 100
    crop_production_index real,
    -- constant 2021 PPP $ per kg of oil equivalent
    gdp_per_unit_of_energy_use real
);
