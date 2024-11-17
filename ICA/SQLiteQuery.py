from DatabaseQueryInterface import DatabaseQueryInterface
import DatabaseManager as db_manager
from Constants import DAILY_WEATHER_TBL, CITY, YEAR, TEMP, PRECIP


class SQLiteQuery(DatabaseQueryInterface):
    
    def __init__(self, db_manager):
        """
        Initialize the SQLiteQuery class with a DatabaseManager instance.
        :param db_manager: Instance of DatabaseManager to handle SQLite connections.
        """
        self.db_manager = db_manager

    def get_average_temperature(self, city_id: int, year: int):
        """
        Fetch the average temperature for a specific city and year.
        :param city_id: The city_id to query.
        :param year: The year to query.
        :return: Average temperature or empty list if no data is available.
        """
        query = f"""
        SELECT AVG({TEMP})
        FROM {DAILY_WEATHER_TBL}
        WHERE {city_id} = ? and {YEAR} = ?
        """
        result = self.db_manager.execute_query(query, (city, year))
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