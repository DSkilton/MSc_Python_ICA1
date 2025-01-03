import logging
from datetime import datetime
from models.daily_weather_entry import DailyWeatherEntry

class WeatherData:
    def __init__(self, weather_data: dict):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Ensure the weather data is a dictionary
        if not isinstance(weather_data, dict):
            self.logger.error(f"Invalid data format: {type(weather_data)}. Expected a dictionary.")
            raise ValueError("weather_data must be a dictionary.")

        self.temperature_2m_max = weather_data.get("temperature_2m_max", [])
        self.temperature_2m_min = weather_data.get("temperature_2m_min", [])
        self.precipitation_sum = weather_data.get("precipitation_sum", [])
        self.dates = weather_data.get("time", [])

        self.logger.debug(f"Weather data initialized with {len(self.dates)} entries.")


    def is_valid(self):
        """
        Validate the structure of the weather data.
        Returns True if all expected fields are present and not empty.
        """
        if not self.temperature_2m_max or not self.temperature_2m_min or not self.precipitation_sum or not self.dates:
            self.logger.error(f"Invalid weather data. Missing or empty required fields: {self.temperature_2m_max}, {self.temperature_2m_min}, {self.precipitation_sum}, {self.dates}")
            return False
        return True


    def is_valid_list(self, weather_data_list):
        """
        Validate the structure of each item in the weather data list.
        Returns True if all items are valid, False otherwise.
        """
        self.logger.debug(f"weather_day, is_valid_list called for {len(weather_data_list)} items")

        for index, weather_data in enumerate(weather_data_list):
            if not weather_data.is_valid():
                self.logger.error(f"Weather data at index {index} is invalid.")
                return False
        return True


    def map_to_daily_weather(self, city_id: int):
        """
        Maps the raw weather data to DailyWeatherEntry objects.
        Returns a list of DailyWeatherEntry objects.
        """
        if not self.is_valid():
            self.logger.error("Invalid weather data. Missing or empty required fields.")
            raise ValueError("Invalid weather data. Missing or empty required fields.")

        self.logger.debug("Mapping raw weather data to DailyWeatherEntry objects...")
        self.logger.debug(f"City ID: {city_id}")

        daily_weather_entries = []

        for date, temp_max, temp_min, precip in zip(
                self.dates,
                self.temperature_2m_max,
                self.temperature_2m_min,
                self.precipitation_sum
        ):

            daily_weather_entries.append(
                DailyWeatherEntry(
                    city_id=city_id,
                    date=datetime.strptime(date, "%Y-%m-%d").date(),
                    min_temp=temp_min,
                    max_temp=temp_max,
                    mean_temp=(temp_max + temp_min) / 2,
                    precipitation=precip
                )
            )

        self.logger.debug(f"Mapped {len(daily_weather_entries)} entries to DailyWeatherEntry objects.")
        return daily_weather_entries


    def __str__(self):
        """
        Returns a string representation of the WeatherData object.
        This can be customized to print out relevant information about the weather data.
        """
        return (f"Weather Data:\n"
                f"Dates: {len(self.dates)} entries\n"
                f"Max Temperatures: {self.temperature_2m_max[:5]}... (first 5)\n"
                f"Min Temperatures: {self.temperature_2m_min[:5]}... (first 5)\n"
                f"Precipitation: {self.precipitation_sum[:5]}... (first 5)")
