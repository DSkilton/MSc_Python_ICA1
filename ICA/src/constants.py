"""
This module defines constants used across the Weather Data Application.

Defines constants used across the Weather Data Application. This module provides 
a single location for managing constants, ensuring consistency and reducing duplication.
"""

# Date
START_OF_YEAR = "-01-01"
END_OF_YEAR = "-12-31"

# Query
SELECT_FROM = "SELECT * FROM "

# table names
DAILY_WEATHER_TBL = "daily_weather_entries"
COUNTRIES_TBL = "countries"
CITIES_TBL = "cities"

# table fields
CITY = "city"
CITY_ID = "city_id"
COUNTRY_ID = "country_id"
PRECIP = "precipitation"
TEMP = "temperature"
DATE = "date"
MEAN_TEMP = "mean_temp"
YEAR = "year"

# Display choices
DISPLAY_CONSOLE = 1
DISPLAY_BAR_CHART = 2
DISPLAY_PIE_CHART = 3
DISPLAY_SCATTER_PLOT = 4
DISPLAY_LINE_CHART = 5

# Main menu options
MENU_VIEW_COUNTRIES = 1
MENU_VIEW_CITIES = 2
MENU_AVG_TEMP = 3
MENU_7DAY_PRECIP = 4
MENU_MEAN_TEMP_CITY = 5
MENU_ANNUAL_PRECIP_CITY = 6
MENU_EXIT = 0

# Labels and Titles for Output
TITLE_COUNTRIES = "Countries"
TITLE_CITIES = "Cities"
TITLE_AVG_TEMP = "Average Temperature"
TITLE_7DAY_PRECIP = "Average Seven-Day Precipitation"
TITLE_MEAN_TEMP_CITY = "Mean Temperature by City"
TITLE_ANNUAL_PRECIP = "Annual Precipitation by Country"

# x Labels for graphs
X_LABEL_COUNTRIES = "Country Name"
X_LABEL_CITIES = "City Name"
X_LABEL_TEMPERATURE = "Temperature"
X_LABEL_PRECIPITATION = "Precipitation"
X_LABEL_YEAR = "Year"

# y Labels for graphs
Y_LABEL_COUNTRY_ID = "Country Id"
Y_LABEL_CITY_ID = "City Id"
Y_LABEL_TEMPERATURE = "Temperature (°C)"
Y_LABEL_PRECIPITATION = "Precipitation (mm)"

ATTEMPT = "attempt"
NAME = "name"
LATITUDE = "latitude"
LONGITUDE = "longitude"
COUNTRY = "country"
TIMEZONE = "timezone"

START_DATE = "start_date"
END_DATE = "end_date"
DAILY = "daily"

TEMPERATURE_2M_MAX = "temperature_2m_max"
TEMPERATURE_2M_MIN = "temperature_2m_min"
PRECIPITATION_SUM = "precipitation_sum"

ID = "id"

MONTH_NAMES = [
        "January", "February", "March", "April", "May", "June", "July", "August", 
        "September", "October", "November", "December"
]
