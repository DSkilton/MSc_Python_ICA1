from ICA.database_query_interface import DatabaseQueryInterface
import ICA.database_manager as db_manager
from constants import *


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
        query = f"""
        SELECT AVG({PRECIP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? AND {DATE} BETWEEN ? AND ?
        """
        end_date = int(start_date) + 6
        result = self.db_manager.execute_query(query, (city_id, start_date, end_date))
        return result[0][0] if result else None
    

    def average_mean_temp_by_city(self, city_id, start_date, end_date):
        query = f"""
        SELECT AVG({MEAN_TEMP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {CITY_ID} = ? AND {DATE} BETWEEN ? AND ? 
        """
        result = self.db_manager.execute_query(query, (city_id, start_date, end_date))
        return result[0][0] if result else None