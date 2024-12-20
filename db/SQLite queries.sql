-- database: ../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db
-- SQLite queries

select * from cities;
select * from countries;
select * from daily_weather_entries;


SELECT * FROM daily_weather_entries 
WHERE city_id = 1 and date = "2020-12-01";

SELECT AVG(precipitation)
FROM daily_weather_entries
WHERE city_id = 1 AND date BETWEEN '2020-01-01' AND '2020-01-07';