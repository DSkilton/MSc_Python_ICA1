import unittest
from unittest.mock import MagicMock
from sqlite_query import SQLiteQuery
from database_manager import DatabaseManager

class TestSQLiteQuery(unittest.TestCase):

    def setUp(self):
        """Set up a mocked DatabaseManager and SQLiteQuery instance."""
        self.mock_db_manager = MagicMock(spec=DatabaseManager)
        self.query = SQLiteQuery(self.mock_db_manager)

    def test_get_all_countries(self):
        """Test retrieving all countries from the database."""
        self.mock_db_manager.execute_query.return_value = [
            {"id": 1, "name": "Country A"}, {"id": 2, "name": "Country B"}
        ]
        results = self.query.get_all_countries()
        self.mock_db_manager.execute_query.assert_called_once_with("SELECT * FROM countries")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "Country A")

    def test_get_average_temperature(self):
        """Test calculating average temperature."""
        self.mock_db_manager.execute_query.return_value = [(20.5,)]
        results = self.query.get_average_temperature(1, 2023)
        self.mock_db_manager.execute_query.assert_called_once()
        self.assertEqual(results, 20.5)

    def test_average_seven_day_precipitation_invalid_date(self):
        """Test handling invalid date input."""
        results = self.query.average_seven_day_precipitation(1, "invalid-date")
        self.assertIsNone(results)

    def test_average_seven_day_precipitation_valid(self):
        """Test calculating average precipitation for valid input."""
        self.mock_db_manager.execute_query.return_value = [(5.2,)]
        results = self.query.average_seven_day_precipitation(1, "2023-01-01")
        self.mock_db_manager.execute_query.assert_called_once()
        self.assertEqual(results, 5.2)

if __name__ == "__main__":
    unittest.main()

