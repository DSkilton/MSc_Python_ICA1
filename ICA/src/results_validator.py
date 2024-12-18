"""
Results Validator

Handles the validation of query results for the Weather Data Application.
"""

import sqlite3

class ResultsValidator:
    """
    Validates query results to ensure they are well-formed and contain data.
    """

    @staticmethod
    def validate(results):
        """
        Validate query results to ensure they contain data.

        Parameters
        ----------
        results : list, float, or None
            Query results from the database. Can be a list of rows, a numeric value, or None.

        Returns
        -------
        bool
            True if results are valid and contain data; otherwise, False.
        """
        if results is None:
            print("No data found.")
            return False

        if isinstance(results, (int, float)):
            return True

        if isinstance(results, list):
            if all(isinstance(row, sqlite3.Row) for row in results) or all(isinstance(row, dict) for row in results):
                return len(results) > 0

        print("Invalid data format.")
        return False
