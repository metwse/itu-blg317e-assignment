-- 1 "users" table
-- -------------------------------------------------------------
CREATE TABLE users (
    id bigserial NOT NULL PRIMARY KEY,
    email text NOT NULL UNIQUE,
    password text NOT NULL,
    name text NOT NULL
);

-- 2 "providers" table
-- -------------------------------------------------------------
CREATE TABLE providers (
    id bigserial NOT NULL PRIMARY KEY,
    administrative_account bigint NOT NULL REFERENCES users (id),
    technical_account bigint REFERENCES users (id),
    name text NOT NULL,
    description text,
    website_url text,
    immutable boolean NOT NULL
);

-- 3 "economies" table
-- -------------------------------------------------------------
CREATE TABLE economies (
    code char(3) NOT NULL PRIMARY KEY,
    name text NOT NULL UNIQUE,
    region char(3) REFERENCES regions (id),
    income_level char(3) REFERENCES income_levels (id),
    is_aggregate bool NOT NULL,
    capital_city text,
    lat real,
    lng real
);

-- 4 "permissions" table
-- permission can be given to a region XOR an economy
-- -------------------------------------------------------------
CREATE TABLE permissions (
    id bigserial PRIMARY KEY,
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    economy_code char(3) REFERENCES economies (code) ON DELETE CASCADE,
    region char(3) REFERENCES regions (id),
    year_start integer NOT NULL,
    year_end integer NOT NULL,
    footnote text,
    created_at timestamp DEFAULT NOW() NOT NULL

    -- 1. either economy OR region, not both, not neither
    CONSTRAINT check_permission_scope_xor
    CHECK (
        (economy_code IS NOT NULL AND region IS NULL) OR
        (economy_code IS NULL AND region IS NOT NULL)
    )
);

-- ensure uniqueness for economy-based permissions
CREATE UNIQUE INDEX idx_permissions_unique_economy
    ON permissions (provider_id, economy_code, year_start, year_end)
    WHERE region IS NULL;

-- ensure uniqueness for region-based permissions
CREATE UNIQUE INDEX idx_permissions_unique_region
    ON permissions (provider_id, region, year_start, year_end)
    WHERE economy_code IS NULL;
