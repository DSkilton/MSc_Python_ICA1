import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch, MagicMock
from output_handler import OutputHandler

class TestOutputHandler(unittest.TestCase):

    @patch("output_handler.OutputHandlerRegistry.get_handler")
    def test_view_all_countries_console(self, mock_get_handler):
        """Test 'View All Countries' with Console Output."""
        mock_console_handler = MagicMock()
        mock_get_handler.return_value = mock_console_handler

        # Simulate country results
        results = [{"id": 1, "name": "Great Britain", "timezone": "Europe/London"},
                   {"id": 2, "name": "France", "timezone": "Europe/Berlin"}]

        OutputHandler.handle_output(1, results, title="Countries")

        # Verify console handler is called with correct data
        mock_console_handler.assert_called_once_with(results)

    @patch("output_handler.OutputHandlerRegistry.get_handler")
    def test_view_all_countries_bar_chart(self, mock_get_handler):
        """Test 'View All Countries' with Bar Chart Output."""
        mock_bar_chart_handler = MagicMock()
        mock_get_handler.return_value = mock_bar_chart_handler

        results = [{"id": 1, "name": "Great Britain", "timezone": "Europe/London"},
                   {"id": 2, "name": "France", "timezone": "Europe/Berlin"}]

        OutputHandler.handle_output(2, results, title="Countries", xlabel="Country Name", ylabel="ID")

        # Verify bar chart handler is called with correct labels and values
        mock_bar_chart_handler.assert_called_once_with(
            ["Great Britain", "France"],  # labels
            [1, 2],                       # values
            "Countries",                  # title
            "Country Name",               # xlabel
            "ID"                          # ylabel
        )

    @patch("output_handler.OutputHandlerRegistry.get_handler")
    def test_view_all_countries_pie_chart(self, mock_get_handler):
        """Test 'View All Countries' with Pie Chart Output."""
        mock_pie_chart_handler = MagicMock()
        mock_get_handler.return_value = mock_pie_chart_handler

        results = [{"id": 1, "name": "Great Britain", "timezone": "Europe/London"},
                   {"id": 2, "name": "France", "timezone": "Europe/Berlin"}]

        OutputHandler.handle_output(3, results, title="Countries")

        # Verify pie chart handler is called with correct data
        mock_pie_chart_handler.assert_called_once_with(
            [1, 1],                       # dummy values for equal slices
            ["Great Britain", "France"],  # labels
            "Countries"                   # title
        )

    @patch("output_handler.OutputHandlerRegistry.get_handler")
    def test_view_all_cities_console(self, mock_get_handler):
        """Test 'View All Cities' with Console Output."""
        mock_console_handler = MagicMock()
        mock_get_handler.return_value = mock_console_handler

        results = [{"id": 1, "name": "Middlesbrough", "longitude": 54.57623, "latitude": -1.23483, "country_id": 1},
                   {"id": 2, "name": "London", "longitude": 51.50853, "latitude": -0.12574, "country_id": 1}]

        OutputHandler.handle_output(1, results, title="Cities")

        # Verify console handler is called with correct data
        mock_console_handler.assert_called_once_with(results)

    @patch("output_handler.OutputHandlerRegistry.get_handler")
    def test_view_all_cities_bar_chart(self, mock_get_handler):
        """Test 'View All Cities' with Bar Chart Output."""
        mock_bar_chart_handler = MagicMock()
        mock_get_handler.return_value = mock_bar_chart_handler

        results = [{"id": 1, "name": "Middlesbrough", "longitude": 54.57623, "latitude": -1.23483, "country_id": 1},
                   {"id": 2, "name": "London", "longitude": 51.50853, "latitude": -0.12574, "country_id": 1}]

        OutputHandler.handle_output(2, results, title="Cities", xlabel="City Name", ylabel="ID")

        # Verify bar chart handler is called with correct labels and values
        mock_bar_chart_handler.assert_called_once_with(
            ["Middlesbrough", "London"],  # labels
            [1, 2],                       # values
            "Cities",                     # title
            "City Name",                  # xlabel
            "ID"                          # ylabel
        )

if __name__ == "__main__":
    unittest.main()
