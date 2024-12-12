"""
This module defines constants used across the Weather Data Application.

Constants include:
- Date strings for the start and end of the year.
- SQL query components for database interactions.
- Table names and field names for the SQLite database.
"""

# Date
START_OF_YEAR = "01/01"
END_OF_YEAR = "31/12/"

# Query
SELECT_FROM = "SELECT * FROM "

# table names
DAILY_WEATHER_TBL = "daily_weather_entries"
COUNTRIES_TBL = "countries"
CITIES_TBL = "cities"

# table fields
CITY = "city"
CITY_ID = "city_id"
PRECIP = "precipitation"
TEMP = "temperature"
DATE = "date"
MEAN_TEMP = "mean_temp"
YEAR = "year"
