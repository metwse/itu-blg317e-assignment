-- Split indicators into three physical tables:
-- `economic_indicators`, `health_indicators`, and `environment_indicators`.
-- A compatibility view `indicators` is provided (FULL OUTER JOIN) so existing
-- queries expecting a single combined table continue to work.
-- -------------------------------------------------------------

-- Economic indicators table
CREATE TABLE economic_indicators (
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    economy_code char(3) NOT NULL REFERENCES economies (code) ON DELETE CASCADE,
    year integer NOT NULL,

    industry real,
    gdp_per_capita real,
    trade real,
    agriculture_forestry_and_fishing real,

    PRIMARY KEY (provider_id, economy_code, year)
);

-- Health indicators table
CREATE TABLE health_indicators (
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    economy_code char(3) NOT NULL REFERENCES economies (code) ON DELETE CASCADE,
    year integer NOT NULL,

    community_health_workers real,
    prevalence_of_undernourishment real,
    prevalence_of_severe_food_insecurity real,
    basic_handwashing_facilities real,
    safely_managed_drinking_water_services real,
    diabetes_prevalence real,

    PRIMARY KEY (provider_id, economy_code, year)
);

-- Environment indicators table
CREATE TABLE environment_indicators (
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    economy_code char(3) NOT NULL REFERENCES economies (code) ON DELETE CASCADE,
    year integer NOT NULL,

    energy_use real,
    access_to_electricity real,
    alternative_and_nuclear_energy real,
    permanent_cropland real,
    crop_production_index real,
    gdp_per_unit_of_energy_use real,

    PRIMARY KEY (provider_id, economy_code, year)
);

-- Compatibility view that presents a single combined view similar to the
-- original `indicators` table. This keeps external queries/code working
-- while the application uses the three tables directly.
CREATE VIEW indicators AS
    SELECT
        COALESCE(ei.provider_id, hi.provider_id, env.provider_id) AS provider_id,
        COALESCE(ei.economy_code, hi.economy_code, env.economy_code) AS economy_code,
        COALESCE(ei.year, hi.year, env.year) AS year,

        ei.industry,
        ei.gdp_per_capita,
        ei.trade,
        ei.agriculture_forestry_and_fishing,

        hi.community_health_workers,
        hi.prevalence_of_undernourishment,
        hi.prevalence_of_severe_food_insecurity,
        hi.basic_handwashing_facilities,
        hi.safely_managed_drinking_water_services,
        hi.diabetes_prevalence,

        env.energy_use,
        env.access_to_electricity,
        env.alternative_and_nuclear_energy,
        env.permanent_cropland,
        env.crop_production_index,
        env.gdp_per_unit_of_energy_use
    FROM economic_indicators ei
    FULL OUTER JOIN health_indicators hi USING (provider_id, economy_code, year)
    FULL OUTER JOIN environment_indicators env USING (provider_id, economy_code, year);

