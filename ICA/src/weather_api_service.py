from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from constants import *
from models import DailyWeatherEntry
from base_api_service import BaseApiService
from weather_data import WeatherData

class WeatherApiService(BaseApiService):
    """
    Service for interacting with the Open-Meteo Weather Data API.
    """
    def __init__(self, session: Session, max_retries=3, retry_delay=2):
        base_url = "https://archive-api.open-meteo.com/v1/archive"
        super().__init__(base_url=base_url, max_retries=max_retries, retry_delay=retry_delay)
        self.session = session


    def fetch_weather_data(self, latitude, longitude, start_date, end_date, city_id):
        """
        Fetch weather data from the Open-Meteo Weather API and store it in the database.

        Parameters
        ----------
        latitude : float
            Latitude of the location.
        longitude : float
            Longitude of the location.
        start_date : str
            Start date for the data (format: yyyy-mm-dd).
        end_date : str
            End date for the data (format: yyyy-mm-dd).
        city_id : int
            ID of the city associated with the weather data.

        Returns
        -------
        dict
            Daily weather data for the specified period.
        """
        self.logger.debug(f"Initial values: {latitude}, {longitude}, {start_date}, {end_date}, {city_id}")
        params = {
            LATITUDE: latitude,
            LONGITUDE: longitude,
            START_DATE: start_date,
            END_DATE: end_date,
            TIMEZONE: "auto",
            DAILY: ','.join([TEMPERATURE_2M_MAX, TEMPERATURE_2M_MIN, PRECIPITATION_SUM]),
        }
        self.logger.debug(f"Request params: {params}")

        try:
            data = self._make_request(params=params)
            # self.logger.debug(f"weather api, data fetched: {data}")

            if "error" in data:
                self.logger.error(f"Weather API returned an error: {data['error']}")
                raise ValueError(f"weather_api, Weather API error: {data['error']}")

            if "daily" in data:
                # Create WeatherData object
                # self.logger.debug(f"Weather data: {data['daily']}")
                weather_data = WeatherData(data["daily"])
                self.logger.debug(f"weather_api, Weather data mapped: {weather_data}")

                if weather_data.is_valid():
                    # self.logger.debug(f"Weather data: {data['daily']}")
                    # self.logger.debug(f"Valid weather data received: {weather_data}")
                    # self.logger.debug(f"weather_api_service, City Id: {city_id}.")

                    daily_weather_entries = weather_data.map_to_daily_weather(city_id)
                    self.logger.debug(f"Daily weather data: {weather_data}")
                    # self.logger.debug(f"api service, daily_weather_entries: {daily_weather_entries}")
                    self._store_weather_data(daily_weather_entries, city_id)
                    return weather_data
                else:
                    self.logger.error("Invalid weather data received.")
                    raise ValueError("Weather data is invalid or incomplete.")
            else:
                raise ValueError("Weather API returned unexpected structure.")
        except Exception as e:
            self.logger.error(f"Weather API Error: {e}")
            return WeatherData({
                TEMPERATURE_2M_MAX: [],
                TEMPERATURE_2M_MIN: [],
                PRECIPITATION_SUM: []
            })


    def _store_weather_data(self, daily_weather_entries, city_id: int):
        """
        Store weather data in the database.

        Parameters
        ----------
        daily_weather_entries : list
            List of DailyWeatherEntry objects to store.
        city_id : int
            ID of the city associated with the weather data.
        """
        try:
            # Add each daily weather entry to the session
            for entry in daily_weather_entries:
                self.session.add(entry)

            self.session.commit()
            self.logger.debug(f"Stored weather data for city ID {city_id}")
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Failed to store weather data: {e}")
            raise
