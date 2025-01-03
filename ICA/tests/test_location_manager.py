from location_manager import LocationManager

class TestLocationManager(unittest.TestCase):

    def setUp(self):
        self.mock_db_manager = MagicMock()
        self.mock_geocoding_service = MagicMock()
        self.mock_weather_service = MagicMock()
        self.manager = LocationManager(self.mock_db_manager, self.mock_geocoding_service, self.mock_weather_service)

    def test_ensure_location_in_database(self):
        """Test ensuring location exists in the database."""
        self.mock_db_manager.city_exists.return_value = False
        self.mock_geocoding_service.fetch_city_data.return_value = {
            "name": "London", "latitude": 51.5, "longitude": -0.12, "country": "UK", "timezone": "GMT"
        }

        result = self.manager.ensure_location_in_database("London")

        self.mock_db_manager.city_exists.assert_called_once_with("London")
        self.mock_geocoding_service.fetch_city_data.assert_called_once_with("London")
        self.mock_db_manager.insert_city.assert_called_once()
        self.assertEqual(result["name"], "London")
