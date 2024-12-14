import unittest
from unittest.mock import patch
from ICA.src.input_handler import InputHandler

class TestInputHandler(unittest.TestCase):
    @patch("builtins.input", side_effect=["abc", "123"])
    def test_get_integer_input(self, mock_input):
        """Test get_integer_input with invalid and valid inputs."""
        result = InputHandler.get_integer_input("Enter a number:")
        self.assertEqual(result, 123)

    @patch("builtins.input", side_effect=["abcd", "2023"])
    def test_get_year_input(self, mock_input):
        """Test get_year_input with invalid and valid inputs."""
        result = InputHandler.get_year_input("Enter a year:")
        self.assertEqual(result, "2023")

    @patch("builtins.input", side_effect=["32/13/2023", "01/01/2022"])
    def test_get_date_input(self, mock_input):
        """Test get_date_input with invalid and valid date formats."""
        result = InputHandler.get_date_input("Enter a date (dd/mm/yyyy):")
        self.assertEqual(result, "01/01/2022")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["Invalid", "20/10/2020"])
    def test_get_date_input_with_output(self, mock_input, mock_print):
        """Test get_date_input and validate print output."""
        result = InputHandler.get_date_input("Enter a date (dd/mm/yyyy):")
        self.assertEqual(result, "20/10/2020")
        mock_print.assert_any_call("Invalid input. Please enter a date in the format dd/mm/yyyy (e.g., 01/01/2021).")

if __name__ == "__main__":
    unittest.main()
