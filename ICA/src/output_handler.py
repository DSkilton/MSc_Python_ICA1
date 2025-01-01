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
        OutputHandler.logger.debug(f"output_handler, type of result: {type(results)}")
        OutputHandler.logger.debug(f"Results standardised: {results}")


        if not isinstance(results, list):
            print("Results should be a list or a numeric value. Falling back to console.")
            OutputHandler._display_table(results)
            return

        labels, values = OutputHandler._extract_labels_values(results)
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
        print(f"output_handler, _display_table: {type(results)}")
        if not results or not isinstance(results, list):
            print("No data to display.")
            return

        # Extract headers dynamically
        headers = list(results[0].keys())

        # Initialize column widths based on header lengths
        column_widths = {header: len(header) for header in headers}

        # Update column widths based on data in rows
        for row in results:
            for header in headers:
                value = row.get(header, "")
                # Ensure id and country_id are treated as integers
                if header in {"id", "country_id"} and value is not None:
                    try:
                        value = int(float(value))
                    except ValueError:
                        value = value   
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
        results : list[City, Country, DailyWeatherEntry] or float
            The query results to standardize.

        Returns
        -------
        list[dict]
            A standardized list of dictionaries with formatted numeric values.
        """
        print(f"output_handler, _standardise_results: {type(results)}")
        
        if isinstance(results, (int, float)):
            return [{"Result": f"{results:.2f}"}]

        if isinstance(results, list):
            standardized = []
            for row in results:
                row_dict = {}
                
                # If row is an instance of SQLAlchemy model, convert to dictionary
                if isinstance(row, City):
                    row_dict["id"] = row.id
                    row_dict["name"] = row.name
                    row_dict["latitude"] = f"{row.latitude:.6f}"
                    row_dict["longitude"] = f"{row.longitude:.6f}"
                    row_dict["timezone"] = row.timezone
                    row_dict["country_id"] = row.country_id
                    row_dict["country_name"] = row.country.name if row.country else None  # Assuming 'Country' relation is set
                elif isinstance(row, Country):
                    row_dict["id"] = row.id
                    row_dict["name"] = row.name
                    row_dict["timezone"] = row.timezone
                elif isinstance(row, DailyWeatherEntry):
                    row_dict["id"] = row.id
                    row_dict["date"] = row.date
                    row_dict["min_temp"] = f"{row.min_temp:.2f}"
                    row_dict["max_temp"] = f"{row.max_temp:.2f}"
                    row_dict["mean_temp"] = f"{row.mean_temp:.2f}"
                    row_dict["precipitation"] = f"{row.precipitation:.2f}"
                    row_dict["city_id"] = row.city_id

                standardized.append(row_dict)
            return standardized
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
    def _extract_labels_values(results):
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
        # Handle empty results
        if not results or not isinstance(results[0], dict):
            return ["No data"], [0]

        # Dynamically extract keys as labels and values
        labels = list(results[0].keys())  # Use the dictionary keys as the labels
        values = [list(row.values()) for row in results]  # Extract the values as the data for plotting

        # Flatten the list of lists (if necessary) and convert all values to floats for graphing
        values = [float(v) if isinstance(v, (int, float)) else 0 for v in values]
        
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
    def convert_to_dicts(rows):
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
