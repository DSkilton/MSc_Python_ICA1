"""
Module for handling user input validation.

This module provides methods for user input validation. It ensures all inputs
are valid before being passed to other parts of the application.
"""
from datetime import datetime
import logging


class InputHandler:
    """
    A utility class for handling and validating user input.
    """

    logger = logging.getLogger(__name__)

    @staticmethod
    def get_integer_input(prompt: str) -> int:
        """
        Prompt the user for an integer input and validate the input.

        Parameters
        ----------
        prompt : str
            The prompt message to display to the user.

        Returns
        -------
        int
            The validated integer input provided by the user.

        Raises
        ------
        ValueError
            If the user input is not a valid integer, the user will be prompted again.
        """
        while True:
            try:
                choice = int(input(prompt))
                if choice < 0:
                    InputHandler.logger.warning(f"Invalid input: {choice}. It must be a positive integer.")
                    raise ValueError("Input must be a positive integer.")
                return choice
            except ValueError:
                InputHandler.logger.warning(f"User entered invalid input. Prompt: {prompt}")
                print("Invalid input. Please enter a valid number.")


    @staticmethod
    def get_year_input(prompt: str) -> str:
        """
        Prompt the user for a year input and validate it as a four-digit year.

        Parameters
        ----------
        prompt : str
            The prompt message to display to the user.

        Returns
        -------st
        str
            The validated year input as a four-character string.

        Notes
        -----
        The year input must consist of exactly four digits (e.g., "2020").
        """
        while True:
            user_input = input(prompt)
            if len(user_input) == 4 and user_input.isdigit():
                return user_input
            print("Invlaid input. Enter a year as 4 digits i.e 2020")


    @staticmethod
    def get_date_input(prompt: str) -> str:
        """
        Prompt the user for a date input and validate it in the format yyyy-mm-dd.

        Parameters
        ----------
        prompt : str
            The prompt message to display to the user.

        Returns
        -------
        str
            The validated date input as a string in the format yyyy-mm-dd.

        Raises
        ------
        ValueError
            If the user input does not conform to the expected date format or is invalid.

        Notes
        -----
        The date must be valid and conform to the format yyyy-mm-dd.
        """
        while True:
            user_input = input(prompt)
            try:
                date = datetime.strptime(user_input, "%Y-%m-%d")
                # Parse the input string to validate it as a date
                if date > datetime.now():
                    print("The start date cannot be in the future. Please try again.")
                    continue
                return date.strftime("%Y-%m-%d")
            except ValueError:
                InputHandler.logging.warning("User entered an invalid date.")
                print("Invalid input. Please enter a date in the format yyyy-mm-dd (e.g., 2021-01-01).")


    @staticmethod
    def get_latitude_longitude(prompt: str) -> float:
        """
        Validate latitude or longitude input ensuring it falls within acceptable ranges.
        Latitude: -90 to 90
        Longitude: -180 to 180
        """
        while True:
            try:
                value = float(input(prompt))
                if 'latitude' in prompt.lower() and -90 <= value <= 90:
                    return value
                elif 'longitude' in prompt.lower() and -180 <= value <= 180:
                    return value
                else:
                    print("Invalid range. Latitude must be -90 to 90, and Longitude must be -180 to 180.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
