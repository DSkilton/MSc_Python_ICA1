import unittest
from unittest.mock import patch, MagicMock
from base_api_service import BaseApiService


class TestBaseApiService(unittest.TestCase):

    @patch("requests.get")
    def test_successful_request(self, mock_get):
        """Test that a successful request returns expected JSON."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"success": True}

        service = BaseApiService(base_url="http://mockapi.com")
        result = service._make_requests(params={"key": "value"})

        self.assertEqual(result, {"success": True})
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_retry_on_failure(self, mock_get):
        """Test retry logic when requests fail."""
        mock_get.side_effect = requests.RequestException("Mock failure")

        service = BaseApiService(base_url="http://mockapi.com", max_retries=2)

        with self.assertRaises(Exception) as context:
            service._make_requests(params={"key": "value"})

        self.assertIn("after 2 attempts", str(context.exception))
        self.assertEqual(mock_get.call_count, 2)
