import sqlite3
import logging
from output_handler_registry import OutputHandlerRegistry

class OutputHandler:
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
        # Standardise the results
        results = OutputHandler._standardise_results(results)

        #Prepare labels and values
        labels, values = OutputHandler._extract_labels_values(results)

        handlers = {
            1: "console",
            2: "bar_chart",
            3: "pie_chart"
        }
        handler_name = handlers.get(choice)
        handler = OutputHandlerRegistry.get_handler(handler_name)

        try:
            if handler_name == "console":
                OutputHandler._display_table(results)
            else:
                # Extract labels and values for graphs
                labels, values = OutputHandler._extract_labels_values(results)
                if handler_name == "pie_chart":
                    handler(values, labels, title)
                else:
                    handler(labels, values, title, xlabel, ylabel)
        except Exception as e:
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
        if not results or not isinstance(results, list):
            print("No data to display.")
            return

        # Extract headers dynamically
        headers = results[0].keys()
        header_line = " | ".join(headers)
        print(f"{header_line}")
        print("-" * len(header_line))

        # Print each row of data
        for result in results:
            row_line = " | ".join(
                str(result.get(key, "N/A")) for key in headers
            )
            print(row_line)


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
    def _standardise_results(results):
        """
        Standardize results to a list format and format numeric values to 2 decimal places.

        Parameters
        ----------
        results : list[sqlite3.Row] or float
            The query results to standardize.

        Returns
        -------
        list[dict]
            A standardized list of dictionaries with formatted numeric values.
        """
        if isinstance(results, (int, float)):
            return [{"Result": f"{results:.2f}"}]  # Format single numeric result to 2 decimal places
        elif isinstance(results, list):
            if isinstance(results[0], sqlite3.Row):
                # Convert sqlite3.Row to dictionary and format numeric values
                return [
                    {key: (f"{value:.2f}" if isinstance(value, (int, float)) else value) 
                    for key, value in dict(row).items()}
                    for row in results
                ]
            else:
                # Format numeric values in list of dictionaries
                return [
                    {key: (f"{value:.2f}" if isinstance(value, (int, float)) else value) 
                    for key, value in result.items()}
                    for result in results
                ]
        return []


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
        if not results or not isinstance(results[0], dict):
            return[], []

        # Default logic
        labels = [str(row.get("name", "unknown")) for row in results]
        values = [row.get("id", row.get("Result", 0)) for row in results]
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
            # TODO: format this a bit better
            print(f"experiend {results:.2f} mm of precipitation")
            return

        # Handle
        if not results or not isinstance(results, list) or not isinstance(results[0], dict):
            print("THIS - if not results or not isinstance(results, list) or not isinstance(results[0], dict): - has been triggered.")
            return

        # Determine the column headers dynamically
        headers = results[0].keys()
        header_line = " | ".join(headers)
        print(f" Header Line: {header_line}")
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
