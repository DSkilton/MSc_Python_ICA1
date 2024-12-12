import unittest
from unittest.mock import patch, MagicMock

from src import WeatherDataApplication
from weather_data_application import WeatherDataApplication
from database_manager import DatabaseManager
from sqlite_query import SQLiteQuery


class TestWeatherDataApplication(unittest.TestCase):
    @patch("ICA.weather_data_application.DatabaseManager")
    @patch("ICA.weather_data_application.SQLiteQuery")
    def setUp(self, mock_sqlite_query, mock_db_manager):
        """
        Set up a test instance of the application with mocked dependencies.
        """
        self.mock_db_manager = mock_db_manager.return_value
        self.mock_query_instance = mock_sqlite_query.return_value
        self.app = WeatherDataApplication("test_db_path")

    def test_select_all_countries(self):
        """
        Test the `select_all_countries` method to ensure it queries and prints correctly.
        """
        self.mock_db_manager.execute_query.return_value = [
            {"id": 1, "name": "Great Britain", "timezone": "Europe/London"}
        ]

        with patch("builtins.print") as mock_print:
            self.app.select_all_countries()
            self.mock_db_manager.execute_query.assert_called_once_with("SELECT * FROM countries")
            mock_print.assert_called_with("Country Id: 1 -- Country Name: Great Britain -- Country Timezone: Europe/London")

    # def test_select_all_cities(self):
    #     """
    #     Test the `select_all_cities` method to ensure it queries and prints correctly.
    #     """
    #     self.mock_db_manager.execute_query.return_value = [
    #         {"id": 1, "name": "Middlesbrough", "country_id": 1}
    #     ]
        
    #     with patch("builtins.print") as mock_print:
    #         self.app.select_all_cities()
    #         self.mock_db_manager.execute_query.assert_called_once_with("SELECT * FROM cities")
    #         mock_print.assert_called_with("City Id: 1 -- City Name: Middlesbrough -- Country Id: 1")

    # @patch("ICA.weather_data_application.InputHandler.get_integer_input", return_value=1)
    # @patch("ICA.weather_data_application.InputHandler.get_year_input", return_value="2021")
    # def test_average_annual_temperature(self, mock_year_input, mock_integer_input):
    #     """
    #     Test the `average_annual_temperature` method for correct query and result handling.
    #     """
    #     self.mock_query_instance.get_average_temperature.return_value = 15.5
        
    #     with patch("builtins.print") as mock_print:
    #         self.app.average_annual_temperature()
    #         self.mock_query_instance.get_average_temperature.assert_called_once_with(city_id=1, date="2021")
    #         mock_print.assert_called_with("Average temperature: 15.5")

    # @patch("ICA.weather_data_application.InputHandler.get_integer_input", side_effect=[1, 20210601])
    # def test_average_seven_day_precipitation(self, mock_input):
    #     """
    #     Test the `average_seven_day_precipitation` method for correct query and result handling.
    #     """
    #     self.mock_query_instance.average_seven_day_precipitation.return_value = 12.3
        
    #     with patch("builtins.print") as mock_print:
    #         self.app.average_seven_day_precipitation()
    #         self.mock_query_instance.average_seven_day_precipitation.assert_called_once_with(1, 20210601)
    #         mock_print.assert_called_with("Average: 12.30")

    def tearDown(self):
        """
        Ensure resources are cleaned up after tests.
        """
        self.app.exit_application()
        self.mock_db_manager.close_connection.assert_called_once()

if __name__ == "__main__":
    unittest.main()
