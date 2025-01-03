import logging

class ConsoleOutputHandler:
    """
    Handles displaying data in the console.
    """

    logger = logging.getLogger(__name__)

    @staticmethod
    def handle_console(results, result_title=None):
        """
        Dynamically chooses the appropriate console display method.

        Parameters
        ----------
        results : list[dict] or float
            The results to display.
        result_title : str, optional
            Title for displaying single result (e.g., 'Average Temperature').
        """
        ConsoleOutputHandler.logger.info(f"console_output_handler, handle_console results: {results[:10]}")
        ConsoleOutputHandler.logger.info(f"console_output_handler, handle_console results: {type(results)}")
        
        # Validate results
        if isinstance(results, (int, float)):  # Handle single numeric results
            ConsoleOutputHandler.display_single_result(result_title, results)
            return
        
        if not results or not isinstance(results, list) or not isinstance(results[0], dict):
            print("No valid data to display.")
            return

        # Extract headers for the table
        headers = list(results[0].keys())
        widths = {header: max(len(header), max(len(str(row.get(header, ''))) for row in results)) for header in headers}

        # Print headers with proper alignment
        header_line = " | ".join(f"{header:<{widths[header]}}" for header in headers)
        separator = "-+-".join("-" * widths[header] for header in headers)
        print(header_line)
        print(separator)

        # Print rows with proper alignment
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

        # Extract headers for the table
        headers = results[0].keys()

        # Calculate column widths
        column_widths = {header: len(header) for header in headers}
        ConsoleOutputHandler.logger.debug(f"Initial column widths (headers): {column_widths}")

        for row in results:
            for header in headers:
                cell_value = str(row.get(header, ""))
                column_widths[header] = max(column_widths[header], len(cell_value))

        ConsoleOutputHandler.logger.debug(f"Final column widths (adjusted): {column_widths}")

        # Format and print headers
        header_line = " | ".join(f"{header:<{column_widths[header]}}" for header in headers)
        separator_line = "-+-".join("-" * column_widths[header] for header in headers)

        print(header_line)
        print(separator_line)

        # Print rows of data with proper alignment
        for row in results:
            row_line = " | ".join(
                f"{str(row.get(header, '')):<{column_widths[header]}}" for header in headers
            )
            print(row_line)

    @staticmethod
    def display_single_result(result_title, result):
        """
        Display a single numeric result with two decimal places.

        Parameters
        ----------
        result_title : str
            Title for the result (e.g., 'Average Temperature').
        result : float or int
            The result to display.
        """
        print(f"{result_title}: {result:.2f}")


    @staticmethod
    def display_monthly_avg_temperature(monthly_data):
        """
        Display monthly average temperature in a formatted table.

        Parameters
        ----------
        monthly_data : dict
            A dictionary where the key is the month (1-12) and the value is the average temperature.
        """
        print(f"Monthly Average Temperature:")
        headers = ['Month', 'Average Temperature (°C)']
        # Find the maximum width needed for the month and average temperature columns
        widths = {
            'Month': len('Month'),
            'Average Temperature (°C)': len('Average Temperature (°C)')
        }
        for month, temp in monthly_data.items():
            widths['Month'] = max(widths['Month'], len(str(month)))
            widths['Average Temperature (°C)'] = max(widths['Average Temperature (°C)'], len(f"{temp:.2f}"))

        # Print headers with proper formatting
        header_line = f"{'Month':<{widths['Month']}} | {'Average Temperature (°C)':<{widths['Average Temperature (°C)']}}"
        separator = f"{'-' * widths['Month']} +- {'-' * widths['Average Temperature (°C)']}"
        print(header_line)
        print(separator)

        # Print each month's data with formatted temperature
        for month, temp in monthly_data.items():
            print(f"{month:<{widths['Month']}} | {temp:.2f}".ljust(widths['Average Temperature (°C)']))
