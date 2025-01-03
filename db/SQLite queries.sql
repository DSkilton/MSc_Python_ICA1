-- database: ../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db
-- SQLite queries

select * from cities;
select * from countries;
select * from daily_weather_entries;

ALTER TABLE daily_weather_entries ADD COLUMN mean_temp REAL;

-- PRAGMA table_info(daily_weather_entries);

select * from daily_weather_entries;

DELETE FROM cities
WHERE id > 5;

DELETE FROM cities;

CREATE TABLE daily_weather_entries (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    min_temp REAL NOT NULL,
    max_temp REAL NOT NULL,
    precipitation REAL NOT NULL,
    city_id INTEGER NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
);

INSERT INTO daily_weather_entries (id, date, min_temp, max_temp, precipitation, city_id)
SELECT id, date, min_temp, max_temp, precipitation, city_id
FROM daily_weather_entries_backup;


CREATE TABLE daily_weather_entries_backup AS SELECT * FROM daily_weather_entries;
DROP TABLE IF EXISTS daily_weather_entries;

PRAGMA index_list('cities');
DROP INDEX IF EXISTS idx_lat_long;


PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;

SELECT * FROM daily_weather_entries 
WHERE city_id = 1 and date = "2020-12-01";

SELECT mean_temp
FROM daily_weather_entries
WHERE city_id = 1 AND date BETWEEN '2020-01-01' AND '2020-12-31';

SELECT AVG(precipitation)
FROM daily_weather_entries
WHERE city_id = 1 AND date BETWEEN '2020-01-01' AND '2020-01-07';

SELECT AVG(mean_temp)
FROM daily_weather_entries
WHERE city_id = 1 AND date BETWEEN '2020-01-01' AND '2020-12-31';

SELECT SUM(precipitation)
FROM daily_weather_entries
WHERE city_id = 1 AND date BETWEEN '2020-01-01' AND '2020-12-31';

SELECT AVG(precipitation)
FROM daily_weather_entries
WHERE city_id = 1 AND date BETWEEN '2020-01-01' AND '2020-01-07';

-- Add additional fields to cities table
ALTER TABLE cities ADD COLUMN population INTEGER;
ALTER TABLE cities ADD COLUMN area REAL;
ALTER TABLE cities ADD COLUMN is_capital BOOLEAN;
ALTER TABLE cities ADD COLUMN country TEXT;
ALTER TABLE cities ADD COLUMN timezone TEXT;

PRAGMA table_info(cities);

CREATE TABLE cities_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    country TEXT,
    timezone TEXT,
    population INTEGER,
    area REAL,
    is_capital BOOLEAN,
    country_id INTEGER NOT NULL
);

INSERT INTO cities_new (id, name, latitude, longitude, country, timezone, population, area, is_capital, country_id)
SELECT id, name, latitude, longitude, country, timezone, population, area, is_capital, country_id
FROM cities;

PRAGMA foreign_keys = OFF;


DROP TABLE cities;
ALTER TABLE cities_new RENAME TO cities;

ALTER TABLE cities
ALTER COLUMN population SET DEFAULT 0,
ALTER COLUMN area SET DEFAULT 0.0,
ALTER COLUMN is_capital SET DEFAULT 0;

PRAGMA table_info(countries);

ALTER TABLE countries
ALTER COLUMN id TYPE INTEGER;

ALTER TABLE cities
ALTER COLUMN id TYPE INTEGER;

SELECT *
FROM daily_weather_entries
WHERE city_id = 6
AND date BETWEEN '2020-01-01' AND '2020-01-07';

SELECT * 
FROM daily_weather_entries
WHERE city_id = 1 
AND date BETWEEN '2020-01-01' AND '2020-01-07';

SELECT c.name, AVG(precipitation) AS average_precipitation
FROM daily_weather_entries d
JOIN cities c ON d.city_id = c.id
WHERE d.city_id = 1
GROUP BY c.name;

SELECT *
FROM daily_weather_entries
WHERE city_id = 1 AND date >= '2020-01-01' AND date <= '2020-01-07';

SELECT AVG(temperature) AS avg_temp
FROM daily_weather_entries
WHERE city_id = ?;

SELECT *
FROM cities
WHERE (latitude, longitude) IN (
    SELECT latitude, longitude
    FROM cities
    GROUP BY latitude, longitude
    HAVING COUNT(*) > 1
);

DELETE FROM cities
WHERE id NOT IN (
    SELECT MIN(id)
    FROM cities
    GROUP BY latitude, longitude
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_lat_long
ON cities(latitude, longitude);
