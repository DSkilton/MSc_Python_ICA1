class TestIntegration(unittest.TestCase):
    """Integration test for fetching and displaying weather data."""

    def test_fetch_weather_data(self):
        """Test end-to-end flow for fetching weather data."""
        db_manager = MagicMock()
        geocoding_service = GeocodingApiService()
        weather_service = WeatherApiService()
        location_manager = LocationManager(db_manager, geocoding_service, weather_service)

        location_manager.ensure_location_in_database = MagicMock(
            return_value={"latitude": 51.5, "longitude": -0.12}
        )
        weather_service.fetch_weather_data = MagicMock(return_value={"temperature": [15, 10], "precipitation": [0, 5]})

        data = location_manager.fetch_location_weather_data("London", "2023-01-01", "2023-01-07")
        self.assertIn("temperature", data)
