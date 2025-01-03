from weather_api_service import WeatherApiService

class TestWeatherApiService(unittest.TestCase):

    @patch("base_api_service.BaseApiService._make_requests")
    def test_fetch_weather_data_success(self, mock_make_requests):
        """Test successful weather data fetch."""
        mock_make_requests.return_value = {
            "daily": {"temperature_2m_max": [15], "temperature_2m_min": [5], "precipitation_sum": [0]}
        }

        service = WeatherApiService()
        result = service.fetch_weather_data(51.5, -0.12, "2023-01-01", "2023-01-07")

        self.assertIn("temperature_2m_max", result)
        self.assertIn("precipitation_sum", result)
        mock_make_requests.assert_called_once_with(
            params={
                "latitude": 51.5,
                "longitude": -0.12,
                "start_date": "2023-01-01",
                "end_date": "2023-01-07",
                "timezone": "auto",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            }
        )

    @patch("base_api_service.BaseApiService._make_requests")
    def test_fetch_weather_data_invalid_response(self, mock_make_requests):
        """Test weather data fetch with invalid response."""
        mock_make_requests.return_value = {}

        service = WeatherApiService()

        with self.assertRaises(ValueError) as context:
            service.fetch_weather_data(51.5, -0.12, "2023-01-01", "2023-01-07")
        self.assertIn("Weather API did not return expected data format", str(context.exception))
