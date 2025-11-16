-- 1 "providers" table
-- -------------------------------------------------------------
CREATE TABLE providers (
    id bigserial NOT NULL PRIMARY KEY,
    email text NOT NULL UNIQUE,
    name text NOT NULL,
    password_hash text NOT NULL,
    nologin boolean NOT NULL,
    is_admin boolean NOT NULL
);

-- 2 "countries" table
-- -------------------------------------------------------------
CREATE TABLE countries (
    code char(3) NOT NULL PRIMARY KEY,
    name text NOT NULL UNIQUE,
    continent continent,
    lat REAL,
    lng REAL
);

-- 3 "permissions" table
-- -------------------------------------------------------------
CREATE TABLE permissions (
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    country_code char(3) NOT NULL REFERENCES countries (code) ON DELETE CASCADE,
    year_start integer NOT NULL,
    year_end integer NOT NULL,

    PRIMARY KEY (provider_id, country_code, year_start, year_end)
);
