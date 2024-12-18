import logging 
from datetime import datetime, timedelta
from database_manager import DatabaseManager
from constants import *
from database_query_interface import DatabaseQueryInterface


# TODO: Add doc string at class level and method level

class SQLiteQuery(DatabaseQueryInterface):
    """
    Handles predefined queries for weather-related data from an SQLite database.

    This class implements the `DatabaseQueryInterface` and provides methods for 
    fetching temperature, precipitation, and other aggregated weather data.
    """

    def __init__(self, db_manager):
        """
        Initialize the SQLiteQuery class with a DatabaseManager instance.
        :param db_manager: Instance of DatabaseManager to handle SQLite connections.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_manager = db_manager


    def get_all_countries(self):
        """
        Retrieve all countries from the database.

        Returns
        -------
        list[dict]
            A list of dictionaries representing all countries.
        """
        query = f"SELECT * FROM {COUNTRIES_TBL}"
        results = self.db_manager.execute_query(query)
        return results
    

    def get_all_cities(self):
        """
        Retrieve all cities from the database.

        Returns
        -------
        list[dict]
            A list of dictionaries representing all cities.
        """
        query = f"SELECT * FROM {CITIES_TBL}"
        results = self.db_manager.execute_query(query)
        return results


    def get_average_temperature(self, city_id: int, year: int):
        """
        Retrieve the average temperature for a specified city and year.

        Parameters
        ----------
        city_id : int
            The ID of the city to query.
        year : int
            The year for which to fetch average temperature data.

        Returns
        -------
        float or None
            The average temperature for the specified city and year, or None if no data is available.
        """
        query = f"""
        SELECT {MEAN_TEMP}
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? and {DATE} BETWEEN ? AND ?
        """
        start_date = f"{year}{START_OF_YEAR}"
        end_date = f"{year}{END_OF_YEAR}"
        self.logger.debug(f"SQLite Query - Fetching average temperature for city_id: {city_id}, year: {year}")
        
        result = self.db_manager.execute_query(query, (city_id, start_date, end_date))
        # self.logger.debug(f"Query result: {result}")
        return result [0][0] if result else []


    def get_precipitation_data(self, city: str, year: int):
        """
        Retrieve the total precipitation for a specified city and year.

        Parameters
        ----------
        city : str
            The name of the city to query.
        year : int
            The year for which to fetch total precipitation data.

        Returns
        -------
        float or None
            Total precipitation for the specified city and year, or None if no data is available.
        """
        self.logger.debug(f"SQLite Query - Fetching average temperature for city: {city}, year= {year}")
        query = f"""
        SELECT SUM({PRECIP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? and {YEAR} = ?
        """
        result = self.db_manager.execute_query(query, (city, year))
        # self.logger.debug(f"Query result: {result}")
        return result[0][0] if result else []


    def average_seven_day_precipitation(self, city_id, start_date):
        """
        Retrieve the average precipitation over a seven-day period for a specified city.

        Parameters
        ----------
        city_id : int
            The ID of the city to query.
        start_date : str
            The start date of the seven-day period (format: yyyy-mm-dd).

        Returns
        -------
        float or None
            The average precipitation over the seven-day period, or None if no data is available.
        """
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = (start_date_obj + timedelta(days=6)).strftime("%Y-%m-%d")

            # Query database
            query = f"""
            SELECT AVG({PRECIP})
            FROM {DAILY_WEATHER_TBL}
            WHERE {CITY_ID} = ? AND {DATE} BETWEEN ? AND ?
            """
            results = self.db_manager.execute_query(query, (city_id, start_date, end_date))
            if results and len(results) > 0 and results[0][0] is not None:
                return results[0][0]
            return None
        except Exception as e:
            self.logger.warning(f"Error while processing dates: {e}")
            return None


    def average_mean_temp_by_city(self, city_id, start_date, end_date):
        """
        Retrieve the mean temperature for a city within a specified date range.

        Parameters
        ----------
        city_id : int
            The ID of the city to query.
        start_date : str
            The start date of the range (format: yyyy-mm-dd).
        end_date : str
            The end date of the range (format: yyyy-mm-dd).

        Returns
        -------
        float or None
            The mean temperature over the specified date range, or None if no data is available.
        """
        query = f"""
        SELECT AVG({MEAN_TEMP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? AND {DATE} BETWEEN ? AND ?
        """
        results = self.db_manager.execute_query(query, (city_id, start_date, end_date))
        if results and len(results) > 0 and results[0][0] is not None:
            return results[0][0]
        return None


    def average_annual_preciption_by_country(self, country_id, year):
        """
        Retrieve the total annual precipitation for all cities in a specified country and year.

        Parameters
        ----------
        country_id : int
            The ID of the country to query.
        year : int
            The year for which to fetch precipitation data.

        Returns
        -------
        float or None
            Total precipitation for the specified country and year, or None if no data is available.
        """
        start_date = f"{year}{START_OF_YEAR}"
        end_date = f"{year}{END_OF_YEAR}"
        query = f"""
        SELECT SUM({PRECIP})
        FROM {DAILY_WEATHER_TBL}
        JOIN {CITIES_TBL} ON {DAILY_WEATHER_TBL}.{CITY_ID} = {CITIES_TBL}.id
        WHERE {CITIES_TBL}.{COUNTRY_ID} = ? AND {DAILY_WEATHER_TBL}.{DATE} BETWEEN ? AND ?;
        """
        results = self.db_manager.execute_query(query, (country_id, start_date, end_date))
        self.logger.debug(f"Country ID: {country_id}, Start Date: {start_date}, End Date: {end_date}")
        if results and len(results) > 0 and results[0][0] is not None:
            return results[0][0]
        return None
