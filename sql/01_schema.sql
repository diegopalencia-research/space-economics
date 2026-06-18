-- ============================================================
-- LAUNCH ECONOMICS & RELIABILITY INTELLIGENCE
-- Evidence System v1.0 | Aerospace Portfolio
-- ============================================================

CREATE TABLE IF NOT EXISTS raw_launches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organisation TEXT,
    location TEXT,
    datum TEXT,
    detail TEXT,
    status_rocket TEXT,
    rocket_cost TEXT,
    status_mission TEXT
);

CREATE TABLE IF NOT EXISTS fact_launches (
    launch_id INTEGER PRIMARY KEY,
    date_launch DATE,
    year_launch INTEGER,
    month_launch INTEGER,
    quarter_launch TEXT,
    dim_organisation_id INTEGER,
    dim_location_id INTEGER,
    dim_rocket_id INTEGER,
    dim_orbit_id INTEGER,
    cost_million REAL,
    payload_mass_kg REAL,
    success_flag INTEGER,
    partial_failure_flag INTEGER,
    FOREIGN KEY (dim_organisation_id) REFERENCES dim_organisation(organisation_id),
    FOREIGN KEY (dim_location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (dim_rocket_id) REFERENCES dim_rocket(rocket_id),
    FOREIGN KEY (dim_orbit_id) REFERENCES dim_orbit(orbit_id)
);

CREATE TABLE IF NOT EXISTS dim_organisation (
    organisation_id INTEGER PRIMARY KEY,
    organisation_name TEXT UNIQUE,
    organisation_type TEXT,
    country_code TEXT,
    founded_year INTEGER,
    market_segment TEXT
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_id INTEGER PRIMARY KEY,
    full_location TEXT UNIQUE,
    site_name TEXT,
    spaceport TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL,
    latitude_category TEXT
);

CREATE TABLE IF NOT EXISTS dim_rocket (
    rocket_id INTEGER PRIMARY KEY,
    rocket_name TEXT UNIQUE,
    rocket_family TEXT,
    reusability_flag INTEGER,
    payload_to_leo_kg REAL,
    payload_to_geo_kg REAL,
    maiden_flight_year INTEGER,
    status TEXT
);

CREATE TABLE IF NOT EXISTS dim_orbit (
    orbit_id INTEGER PRIMARY KEY,
    orbit_class TEXT,
    orbit_description TEXT,
    typical_altitude_km REAL,
    inclination_range TEXT
);
