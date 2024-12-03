# TODO: Add doc string at class level and method level
"""
This module will handle the formatting of any outputs
"""

class OutputHandler:
    """
    Used to format reals to 2 decimal places
    :param number: the numbr to be formatted
    :return: the number formatted to 2 decimal places
    """
    @staticmethod
    def format_two_decimals(number):
        return {f"{number:.2f}"}