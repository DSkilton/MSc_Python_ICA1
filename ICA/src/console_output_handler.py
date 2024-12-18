"""
Console Output Handler

Provides functionality for displaying data in the console.
"""

class ConsoleOutputHandler:
    """
    Handles displaying data in the console.
    """

    @staticmethod
    def handle_console(results, **kwargs):
        """
        Dynamically chooses the appropriate console display method.

        Parameters
        ----------
        results : list[dict] or float
            The results to display.
        kwargs : dict
            Additional arguments, such as `result_title` for single results.
        """
        if isinstance(results, (int, float)):
            ConsoleOutputHandler.display_single_result(
                kwargs.get("result_title", "Result"), results
            )
        elif isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict):
            ConsoleOutputHandler.display_table(results)
        else:
            print("No valid data to display.")


    @staticmethod
    def display_table(results):
        """
        Display a list of results in tabular format.

        Parameters
        ----------
        results : list[dict]
            A list of dictionaries representing rows of data.
        """
        if not results:
            print("No data available to display.")
            return

        # Dynamically extract column headers
        headers = results[0].keys()
        header_line = " | ".join(headers)
        print(header_line)
        print("-" * len(header_line))

        # Print each row of data
        for row in results:
            row_line = " | ".join(str(row.get(key, "N/A")) for key in headers)
            print(row_line)


    @staticmethod
    def display_single_result(result_title, result):
        """
        Display a single numeric result.

        Parameters
        ----------
        result : float or int
            The result to display.
        """
        print(f"{result_title}: {result:.2f}")
