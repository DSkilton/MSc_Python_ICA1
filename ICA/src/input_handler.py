"""
Module for handling user input validation.

This module provides utility methods for validating and retrieving user input.
"""
import datetime


class InputHandler:
    """
    A utility class for handling and validating user input.

    Methods
    -------
    get_integer_input(prompt: str) -> int
        Prompt the user for an integer input and validate the input.
    get_year_input(prompt: str) -> str
        Prompt the user for a year input and validate it as a four-digit year.
    get_date_input(prompt: str) -> str
        Prompt the user for a date input and validate it in the format dd/mm/yyyy.
    """


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
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid integer")


    @staticmethod
    def get_year_input(prompt: str) -> str:
        """
        Prompt the user for a year input and validate it as a four-digit year.

        Parameters
        ----------
        prompt : str
            The prompt message to display to the user.

        Returns
        -------
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
        Prompt the user for a date input and validate it in the format dd/mm/yyyy.

        Parameters
        ----------
        prompt : str
            The prompt message to display to the user.

        Returns
        -------
        str
            The validated date input as a string in the format dd/mm/yyyy.

        Raises
        ------
        ValueError
            If the user input does not conform to the expected date format or is invalid.

        Notes
        -----
        The date must be valid and conform to the format dd/mm/yyyy.
        """
        while True:
            user_input = input(prompt)
            try:
                # Parse the input string to validate it as a date
                datetime.datetime.strptime(user_input, "%d/%m/%Y")
                return user_input
            except ValueError:
                print("Invalid input. Please enter a date in the format dd/mm/yyyy (e.g., 01/01/2021).")

