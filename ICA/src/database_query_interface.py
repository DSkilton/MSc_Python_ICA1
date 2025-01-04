from abc import ABC, abstractmethod

class DatabaseQueryInterface(ABC):
    """
    Abstract base class for querying database weather data.

    Provides a blueprint for fetching temperature and precipitation information
    for specific cities and years. Concrete implementations should provide
    the logic for interacting with their respective data sources.
    """

    @abstractmethod
    def get_average_temperature(self, city_id: int, year: int):
        """
        Fetch the average temperature for a given city and year.

        Parameters
        ----------
        city_id : int
            The ID of the city to query.
        year : int
            The year for which to fetch the data.

        Returns
        -------
        float
            The average temperature for the specified city and year.
        """
        pass

    @abstractmethod
    def get_precipitation_data(self, city_id: int, year: int):
        """
        Fetch the total precipitation data for a given city and year.

        Parameters
        ----------
        city_id : int
            The ID of the city to query.
        year : int
            The year for which to fetch the data.

        Returns
        -------
        float
            The total precipitation for the specified city and year.
        """
        pass

    @abstractmethod
    def average_seven_day_precipitation(self, city_id: int, start_date: str):
        """
        Fetch the average precipitation over a seven-day period.

        Parameters
        ----------
        city_id : int
            The ID of the city to query.
        start_date : str
            The starting date for the seven-day period (format: yyyy-mm-dd).

        Returns
        -------
        float
            The average precipitation over the period.
        """
        pass

    @abstractmethod
    def average_temp_by_city(self, city_id: int, start_date: str, end_date: str):
        """
        Fetch the mean temperature for a city within a date range.

        Parameters
        ----------
        city_id : int
            The ID of the city to query.
        start_date : str
            The start date for the range.
        end_date : str
            The end date for the range.

        Returns
        -------
        float
            The mean temperature within the specified range.
        """
        pass

    @abstractmethod
    def average_annual_precipitation_by_country(self, country_id: int, year: int):
        """
        Fetch the annual precipitation for all cities in a specified country.

        Parameters
        ----------
        country_id : int
            The ID of the country.
        year : int
            The year to query.

        Returns
        -------
        float
            The total precipitation for the specified country and year.
        """
        pass

    @abstractmethod
    def does_city_exist(self, city_name: str):
        """
        Check if a city exists in the database.

        Parameters
        ----------
        city_name : str
            The name of the city.

        Returns
        -------
        bool
            True if the city exists, False otherwise.
        """
        pass

    @abstractmethod
    def insert_city(self, city_data: dict):
        """
        Insert a new city into the database.

        Parameters
        ----------
        city_data : dict
            Dictionary containing city information (name, latitude, longitude, country, timezone).
        """
        pass

    @abstractmethod
    def get_country_id_by_name(self, country_name: str):
        """
        Retrieve the ID of a country based on its name.

        Parameters
        ----------
        country_name : str
            The name of the country.

        Returns
        -------
        int or None
            The ID of the country, or None if not found.
        """
        pass
