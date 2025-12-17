-- "region" type
CREATE TABLE regions (
    id char(3) NOT NULL PRIMARY KEY,
    name text NOT NULL
);

INSERT INTO regions VALUES
    ('LCN', 'Latin America & Caribbean'),
    ('MEA', 'Middle East, North Africa, Afghanistan & Pakistan'),
    ('SSF', 'Sub-Saharan Africa'),
    ('ECS', 'Europe & Central Asia'),
    ('EAS', 'East Asia & Pacific'),
    ('SAS', 'South Asia'),
    ('NAC', 'North America');

-- "income_levels" type
CREATE TABLE income_levels (
    id char(3) NOT NULL PRIMARY KEY,
    name text NOT NULL
);

INSERT INTO income_levels VALUES
    ('HIC', 'High income'),
    ('LIC', 'Low income'),
    ('LMC', 'Lower middle income'),
    ('UMC', 'Upper middle income'),
    ('INX', 'Not classified');
