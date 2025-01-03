from geocoding_api_service import GeocodingApiService

class TestGeocodingApiService(unittest.TestCase):

    @patch("base_api_service.BaseApiService._make_requests")
    def test_fetch_city_data_success(self, mock_make_requests):
        """Test successful city data fetch."""
        mock_make_requests.return_value = {
            "results": [{"name": "London", "latitude": 51.5, "longitude": -0.12, "country": "UK", "timezone": "GMT"}]
        }

        service = GeocodingApiService()
        result = service.fetch_city_data("London")

        self.assertEqual(result["name"], "London")
        self.assertEqual(result["latitude"], 51.5)
        mock_make_requests.assert_called_once_with(params={"name": "London"})

    @patch("base_api_service.BaseApiService._make_requests")
    def test_fetch_city_data_no_results(self, mock_make_requests):
        """Test city data fetch with no results."""
        mock_make_requests.return_value = {"results": []}

        service = GeocodingApiService()

        with self.assertRaises(ValueError) as context:
            service.fetch_city_data("NonexistentCity")
        self.assertIn("No results found", str(context.exception))
