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

-- 2 "economies" table
-- -------------------------------------------------------------
CREATE TABLE economies (
    code char(3) NOT NULL PRIMARY KEY,
    name text NOT NULL UNIQUE,
    region region
);

-- 3 "permissions" table
-- -------------------------------------------------------------
CREATE TABLE permissions (
    provider_id bigint NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
    economy_code char(3) NOT NULL REFERENCES economies (code) ON DELETE CASCADE,
    year_start integer NOT NULL,
    year_end integer NOT NULL,

    PRIMARY KEY (provider_id, economy_code, year_start, year_end)
);
