import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from ICA.src.main import WeatherDataApplication
from ICA.src.database_manager import DatabaseManager
from ICA.src.sqlite_query import SQLiteQuery
from ICA.src.input_handler import InputHandler
from ICA.src.output_handler import OutputHandler

class TestWeatherDataApplication(unittest.TestCase):

    @patch("src.weather_data_application.DatabaseManager")
    @patch("src.weather_data_application.SQLiteQuery")
    def setUp(self, mock_sqlite_query, mock_db_manager):
        """
        Set up a test instance of the application with mocked dependencies.
        """
        self.mock_db_manager = mock_db_manager.return_value
        self.mock_query_instance = mock_sqlite_query.return_value
        self.app = WeatherDataApplication("test_db_path")


    @patch("builtins.print")
    def test_select_all_countries(self, mock_print):
        """
        Test the `select_all_countries` method to ensure it queries and prints correctly.
        """
        self.mock_db_manager.execute_query.return_value = [
            {"id": 1, "name": "Great Britain", "timezone": "Europe/London"}
        ]
        self.app.select_all_countries()
        self.mock_db_manager.execute_query.assert_called_once_with("SELECT * FROM countries")
        mock_print.assert_called_with("Country Id: 1 -- Country Name: Great Britain -- Country Timezone: Europe/London")


    @patch("builtins.print")
    def test_select_all_cities(self, mock_print):
        """
        Test the `select_all_cities` method to ensure it queries and prints correctly.
        """
        self.mock_db_manager.execute_query.return_value = [
            {"id": 1, "name": "Middlesbrough", "country_id": 1}
        ]
        self.app.select_all_cities()
        self.mock_db_manager.execute_query.assert_called_once_with("SELECT * FROM cities")
        mock_print.assert_called_with("City Id: 1 -- City Name: Middlesbrough -- Country Id: 1")


    @patch("src.weather_data_application.InputHandler.get_integer_input", return_value=1)
    @patch("src.weather_data_application.InputHandler.get_year_input", return_value="2021")
    @patch("builtins.print")
    def test_average_annual_temperature(self, mock_print, mock_year_input, mock_integer_input):
        """
        Test the `average_annual_temperature` method for correct query and result handling.
        """
        self.mock_query_instance.get_average_temperature.return_value = 15.5
        self.app.average_annual_temperature()
        self.mock_query_instance.get_average_temperature.assert_called_once_with(city_id=1, date="2021")
        mock_print.assert_called_with("Average temperature: 15.5")


    @patch("src.weather_data_application.InputHandler.get_integer_input", return_value=1)
    @patch("src.weather_data_application.InputHandler.get_date_input", return_value="01/06/2021")
    @patch("builtins.print")
    def test_average_seven_day_precipitation(self, mock_print, mock_date_input, mock_integer_input):
        """
        Test the `average_seven_day_precipitation` method for correct query and result handling.
        """
        self.mock_query_instance.average_seven_day_precipitation.return_value = 12.3
        self.app.average_seven_day_precipitation()
        self.mock_query_instance.average_seven_day_precipitation.assert_called_once_with(1, "01/06/2021")
        mock_print.assert_called_with("Average seven-day precipitation: 12.30 mm")


    @patch("src.weather_data_application.InputHandler.get_integer_input", side_effect=[1, "01/06/2021", "07/06/2021"])
    @patch("builtins.print")
    def test_average_mean_temp_by_city(self, mock_print, mock_inputs):
        """
        Test the `average_mean_temp_by_city` method for correct query and result handling.
        """
        self.mock_query_instance.average_mean_temp_by_city.return_value = 16.5
        self.app.average_mean_temp_by_city()
        self.mock_query_instance.average_mean_temp_by_city.assert_called_once_with(1, "01/06/2021", "07/06/2021")
        mock_print.assert_called_with("Result: 16.5")


    def test_exit_application(self):
        """
        Test the `exit_application` method to ensure it closes the database connection.
        """
        self.app.exit_application()
        self.mock_db_manager.close_connection.assert_called_once()


    def tearDown(self):
        """
        Ensure resources are cleaned up after tests.
        """
        self.mock_db_manager.close_connection.assert_called_once()


if __name__ == "__main__":
    unittest.main()
