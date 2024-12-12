from database_query_interface import DatabaseQueryInterface
import database_manager as db_manager
from constants import *

# TODO: Add doc string at class level and method level

class SQLiteQuery(DatabaseQueryInterface):


    def __init__(self, db_manager):
        """
        Initialize the SQLiteQuery class with a DatabaseManager instance.
        :param db_manager: Instance of DatabaseManager to handle SQLite connections.
        """
        self.db_manager = db_manager


    def get_average_temperature(self, city_id: int, date: int):
        """
        Fetch the average temperature for a specific city and year.
        :param city_id: The city_id to query.
        :param year: The year to query.
        :return: Average temperature or empty list if no data is available.
        """
        query = f"""
        SELECT {MEAN_TEMP}
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? and {DATE} = ?
        """
        result = self.db_manager.execute_query(query, (city_id, date))
        return result [0][0] if result else []


    def get_precipitation_data(self, city: str, year: int):
        """
        Fetch the total precipitation for a specific city and year.
        :param city: The city to query.
        :param year: The year to query.
        :return: Total precipitation or empty list if no data is available.
        """
        query = f"""
        SELECT SUM({PRECIP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY} = ? and {YEAR} = ?
        """
        result = self.db_manager.execute_query(query, (city, year))
        return result[0][0] if result else []


    def average_seven_day_precipitation(self, city_id, start_date):
        """
        Fetch the seven day precipitation for a specific seven day period.
        :param city_id: The city id to query.
        :param start_date: The start of the seven day period.
        :return: Total precipitation or empty list if no data is available.
        """
        query = f"""
        SELECT AVG({PRECIP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? AND {DATE} BETWEEN ? AND ?
        """
        end_date = int(start_date) + 6
        results = self.db_manager.execute_query(query, (city_id, start_date, end_date))
        return results[0][0] if results else None


    def average_mean_temp_by_city(self, city_id, start_date, end_date):
        """
        Fetch the mean temperature for a user defined period or time.
        :param city_id: The city id to query.
        :param start_date: The start date for the query
        :param end_date: The end date for the query
        :return: Average mean temp or empty list if no data is available.
        """
        query = f"""
        SELECT AVG({MEAN_TEMP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? AND {DATE} BETWEEN ? AND ?
        """
        results = self.db_manager.execute_query(query, (city_id, start_date, end_date))
        return results[0][0] if results else None


    def average_annual_preciption_by_country(self, city_id, year):
        """
        Fetch the annual precipitation for a specific city and year.
        :param city_id: The city id to query.
        :param start_date: The year to query
        :return: Average annual precipitation or empty list if no data is available.
        """
        start_date = START_OF_YEAR + year
        end_date = END_OF_YEAR + year
        query = f"""
        SELECT SUM({PRECIP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? AND {DATE} BETWEEN ? AND ?
        """
        results = self.db_manager.execute_query(query, (city_id, start_date, end_date))
        return results[0][0] if results else None
