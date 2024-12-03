"""
This Module handles any formatted output 
"""

class OutputHandler:
    """
    Handles the formatting of outputs, including numbers and strings.

    Methods: 
        format_two_decimals(number):
            Formats the passed number to 2 decimal places.
        format_string(template, **kwargs):
            Formats a string using a template with placeholders.
    """

    @staticmethod
    def format_two_decimals(number):
        """
        Format a number to 2 decimal places.

        Parameters
        ----------
        number : float
            The number to format.

        Returns
        -------
        str
            The number formatted to 2 decimal places as a string.
        """
        return f"{number:.2f}"
