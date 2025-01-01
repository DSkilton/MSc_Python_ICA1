import logging

"""
Console Output Handler

Provides functionality for displaying data in the console.
"""

class ConsoleOutputHandler:
    """
    Handles displaying data in the console.
    """

    logger = logging.getLogger(__name__)

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

        ConsoleOutputHandler.logger.info(f"console_output_handler, handle_console results: {results}")
        # Validate results
        if not results or not isinstance(results, list) or not isinstance(results[0], dict):
            print("No valid data to display.")
            return

        # Extract headers
        headers = list(results[0].keys())
        widths = {header: max(len(header), max(len(str(row.get(header, ''))) for row in results)) for header in headers}

        # Print headers
        header_line = " | ".join(f"{header:<{widths[header]}}" for header in headers)
        separator = "-+-".join("-" * widths[header] for header in headers)
        print(header_line)
        print(separator)

        # Print rows
        for row in results:
            print(" | ".join(f"{str(row.get(header, '')):<{widths[header]}}" for header in headers))


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
            ConsoleOutputHandler.logger.warning("No data available to display.")
            return

        # Extract headers
        headers = results[0].keys()

        # Calculate column widths
        column_widths = {header: len(header) for header in headers}
        ConsoleOutputHandler.logger.debug(f"Initial column widths (headers): {column_widths}")

        for row in results:
            for header in headers:
                cell_value = str(row.get(header, ""))
                column_widths[header] = max(column_widths[header], len(cell_value))

        ConsoleOutputHandler.logger.debug(f"Final column widths (adjusted): {column_widths}")

        header_line = " | ".join(f"{header:<{column_widths[header]}}" for header in headers)
        separator_line = "-+-".join("-" * column_widths[header] for header in headers)

        print(header_line)
        print(separator_line)

        # Print rows of data
        for row in results:
            row_line = " | ".join(
                f"{str(row.get(header, '')):<{column_widths[header]}}" for header in headers
            )
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
