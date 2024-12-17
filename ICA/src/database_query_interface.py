"""
Interface for database query operations.

Defines the structure for querying weather-related data. 
All concrete implementations must define the abstract methods.
"""
from abc import ABC, abstractmethod


class DatabaseQueryInterface(ABC):
    """
    Abstract base class for querying database weather data.

    Provides a blueprint for fetching temperature and precipitation information
    for specific cities and years. Concrete implementations should provide
    the logic for interacting with their respective data sources.
    """
    @abstractmethod
    def get_average_temperature(self, city: str, year: int):
        """
        Fetch the average temperature for a given city and year.

        Parameters
        ----------
        city : str
            The name of the city to query.
        year : int
            The year for which to fetch the data.

        Returns
        -------
        float
            The average temperature for the specified city and year.
        """


    @abstractmethod
    def get_precipitation_data(self, city: str, year: int):
        """
        Fetch the total precipitation data for a given city and year.

        Parameters
        ----------
        city : str
            The name of the city to query.
        year : int
            The year for which to fetch the data.

        Returns
        -------
        float
            The total precipitation for the specified city and year.
        """

    @abstractmethod
    def average_seven_day_precipitation(self, city_id: int, start_date: str):
        pass


    @abstractmethod
    def average_mean_temp_by_city(self, city_id: int, start_date: str, end_date: str):
        pass
    

    @abstractmethod
    def average_annual_preciption_by_country(self, country_id: int, year: int):
        pass
