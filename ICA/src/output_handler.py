import sqlite3
import logging
from models.city import City
from models.country import Country
from models.daily_weather_entry import DailyWeatherEntry
from output_handler_registry import OutputHandlerRegistry

class OutputHandler:
    """
    Provides methods to display results in the console.
    """

    logger = logging.getLogger(__name__)

    @staticmethod
    def handle_output(choice, results, title=None, xlabel=None, ylabel=None):
        """
        Delegates output handling based on the user's choice.

        Parameters
        ----------
        choice : int
            The display choice (i.e., 1 for console, 2 for bar chart, etc.).
        results : list[sqlite3.Row] or single numberic value
            The data to display.
        title : str, optional
            The title for graphical outputs.
        xlabel : str, optional
            The x-axis label for graphical outputs.
        ylabel : str, optional
            The y-axis label for graphical outputs.
        """
        if not results:
            print("No data available.")
            OutputHandler.logger.warning("No data available.")
            return

        results = OutputHandler._standardise_results(results)
        # OutputHandler.logger.debug(f"output_handler, type of result: {type(results)}")
        # OutputHandler.logger.debug(f"Results standardised: {results}")


        if not isinstance(results, list):
            print("Results should be a list or a numeric value. Falling back to console.")
            OutputHandler._display_table(results)
            return

        labels, values = OutputHandler._extract_labels_values_for_cities_and_countries(results)
        handlers = {
            1: "console",
            2: "bar_chart",
            3: "pie_chart"
        }
        handler_name = handlers.get(choice)
        handler = OutputHandlerRegistry.get_handler(handler_name)
        OutputHandler.logger.debug(f"Handler selected: {handler_name}")

        try:
            if handler_name == "console":
                OutputHandler._display_table(results)
            elif handler:
                OutputHandler.logger.debug(f"Graphing with labels: {labels} and values: {values}")
                handler(labels, values, title, xlabel, ylabel)
            else:
                raise ValueError(f"Unsupported output type: {handler_name}")
        except Exception as e:
            OutputHandler.logger.error(f"Error during output handling. Handler: {handler_name}, Choice: {choice}, Error: {e}")
            print(f"Error: Unable to generate chart. {e}")
            print("Falling back to console output.")
            OutputHandler._display_table(results)


    @staticmethod
    def _display_table(results):
        """
        Display results in tabular format, ensuring numeric values are formatted to 2 decimal places.

        Parameters
        ----------
        results : list[dict]
            The tabular results to display.
        """
        print(f"output_handler, _display_table: {type(results)}, {results[:5]}")
        if not results or not isinstance(results, list):
            print("No data to display.")
            return

        # Extract headers dynamically
        headers = list(results[0].keys())

        # Initialize column widths based on header lengths
        column_widths = {header: len(header) for header in headers}

        # Update column widths based on data in rows
        for row in results:
            OutputHandler.logger.debug(f"output_handler, row: {row}")
            for header in headers:
                OutputHandler.logger.debug(f"output_handler, header: {header}")
                value = row.get(header, "")
                OutputHandler.logger.debug(f"output_handler, value: {value}")

                # Ensure id and country_id are treated as integers
                if header in {"id", "country_id"} and value is not None:
                    try:
                        value = int(float(value))
                        OutputHandler.logger.debug(f"Value of type: {type(value)}, {value}")
                    except ValueError:
                        value = value

                # Format numeric values to 2 decimal places (for Temperature)
                if isinstance(value, (int, float)):
                    value = round(value, 2)
                    value = f"{value:.2f}"

                column_widths[header] = max(column_widths[header], len(str(value)))

        # Create format string for headers and rows
        header_format = " | ".join(f"{{:<{column_widths[header]}}}" for header in headers)
        separator = "-+-".join("-" * column_widths[header] for header in headers)

        # Print the header
        print(header_format.format(*headers))
        print(separator)

        # Print each row
        for row in results:
            row_values = [
                str(int(row.get(header, 0))) if header in {"id", "country_id"} and row.get(header) is not None
                else str(row.get(header, "N/A"))
                for header in headers
            ]
            print(header_format.format(*row_values))


    @staticmethod
    def _standardise_results(results):
        """
        Standardize results to a list format and format numeric values to 2 decimal places.

        Parameters
        ----------
        results : list[City, Country, DailyWeatherEntry] or float or dict
            The query results to standardize.

        Returns
        -------
        list[dict]
            A standardised list of dictionaries with formatted numeric values.
        """
        OutputHandler.logger.debug(f"Standardising results of type: {type(results)}")

        # If results is a numeric type (int or float), return it as a formatted dictionary
        if isinstance(results, (int, float)):
            return [{"Result": f"{results:.2f}"}]

        # If results is a dictionary (e.g., monthly data)
        if isinstance(results, dict):
            OutputHandler.logger.debug("Result is a dictionary")
            # Convert dictionary into a list of dictionaries, each containing 'Month' and 'Temperature'
            return [{"Month": month, "Temperature": f"{temp:.2f}"} for month, temp in results.items()]

        # Check if results is a list
        if isinstance(results, list):
            standardised = []

            for row in results:
                # Handle the case where the row is an instance of a model (City, Country, DailyWeatherEntry)
                if isinstance(row, (City, Country, DailyWeatherEntry)):
                    if hasattr(row, 'to_dict'):  # Ensure the row has the to_dict method
                        standardised.append(row.to_dict())
                    else:
                        OutputHandler.logger.debug("We have a problem: No to_dict method found.")
                # If the row is already a dictionary (for example, from the database or API)
                elif isinstance(row, dict):
                    OutputHandler.logger.debug("Row is already a dictionary")
                    standardised.append(row)

            return standardised

        # If results is neither a numeric value nor a dictionary/list, return an empty list
        OutputHandler.logger.debug("No results to standardise")
        return []


    @staticmethod
    def _display_single_result(result):
        """
        Display a single numeric result formatted to 2 decimal places

        Parameters
        ----------
        result : float
            The numeric result to display.
        """
        print(f"Result: {result:.2f}")


    @staticmethod
    def _extract_labels_values_for_cities_and_countries(results):
        """
        Extract labels and values for graphs.

        Parameters
        ----------
        results : list[dict]
            Query results as a list of dictionaries.

        Returns
        -------
        tuple[list, list]
            A tuple containing labels (x-axis) and values (y-axis) for charts.
        """

        OutputHandler.logger.debug(f"extracting labels for results of type: {type(results[0])}, {results[:5]}")

        # Handle empty results
        if not results or not isinstance(results[0], dict):
            return ["No data"], [0]

        # Dynamically extract keys as labels and values
        labels = list(results[0].keys())

        if isinstance(results[0], dict) and "Month" in results[0]:
            # If it's a dictionary with 'Month' and 'Temperature'
            values = [row["Temperature"] for row in results]
            labels = [row["Month"] for row in results]
        else:
            values = [list(row.values()) for row in results]
            labels = [list(row.keys()) for row in results]

        OutputHandler.logger.debug(f"output_handler, labels: {labels}, values: {values}, of type: {type(values)}")

        return labels, values


    @staticmethod
    def handle_console(results):
        """
        Display the results in the console.

        Parameters
        ----------
        results : list[dict] or single numeric value
            Data to display in the console.
        """
        # Handle single numeric results
        if isinstance(results, (int, float)):
            print(f"Experiencing {results:.2f} mm of precipitation")
            return

        # Handle empty results or non-dictionary results
        if not results or not isinstance(results, list) or not isinstance(results[0], dict):
            print("No valid data available.")
            return

        # Determine the column headers dynamically
        headers = results[0].keys()
        header_line = " | ".join(headers)
        print(f"Header Line: {header_line}")
        print("-" * len(header_line))

        # Print each row of data
        for result in results:
            row_line = " | ".join(str(result.get(key, "N/A")) for key in headers)
            print(row_line)


    @staticmethod
    def sqlite_row_to_dict(rows):
        """
        Converts a list of sqlite3.Row objects to a list of standard dictionaries.

        Parameters
        ----------
        rows : list[sqlite3.Row]
            The rows fetched from the SQLite database.

        Returns
        -------
        list[dict]
            A list of dictionaries representing the rows.
        """
        return [dict(row) for row in rows]
