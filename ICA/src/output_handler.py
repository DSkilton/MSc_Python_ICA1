import sqlite3
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
        results : list[sqlite3.Row]
            The data to display.
        title : str, optional
            The title for graphical outputs.
        xlabel : str, optional
            The x-axis label for graphical outputs.
        ylabel : str, optional
            The y-axis label for graphical outputs.
        """

        if not results:
            print("Error: Invalid or empty dataset.")
            OutputHandler.handle_console([])  # Fallback to an empty console display
            return
        
        if not isinstance(results, list):
            data = [data]

        # Convert sqlite3.Row objects to dictionaries if necessary
        if isinstance(results[0], sqlite3.Row):
            results = [dict(row) for row in results]

        handlers = {
            1: "console",
            2: "bar_chart",
            3: "pie_chart"
        }
        handler_name = handlers.get(choice)
        handler = OutputHandlerRegistry.get_handler(handler_name)

        if handler:
            try:
                # TODO: Change the below to constants
                if "Date Range" in results[0] and "Precipitation (mm)" in results[0]:
                    labels = [row["Date Range"] for row in results]
                    values = [row["Precipitation (mm)"] for row in results]
                elif "name" in results[0] and "id" in results[0]:
                    labels = [row["name"] for row in results]
                    values = [row["id"] for row in results]
                else:
                    raise KeyError("Unsupported data structure in results.")

                if handler_name == "console":
                    handler(results)
                elif handler_name == "pie_chart":
                    handler(values, labels, title)
                else:
                    handler(labels, values, title, xlabel, ylabel)
            except Exception as e:
                print(f"Error: Unable to generate chart. {e}")
                print("Falling back to console output.")
                OutputHandler.handle_console(results)
        else:
            print("Invalid choice. Defaulting to console output.")
            OutputHandler.handle_console(results)


    @staticmethod
    def handle_console(results):
        """
        Display the results in the console.

        Parameters
        ----------
        results : list[dict]
            Data to display in the console.
        """
        if not results or not isinstance(results, list) or not isinstance(results[0], dict):
            print("No valid results to display.")
            return

        # Determine the column headers dynamically
        headers = results[0].keys()
        header_line = " | ".join(headers)
        print(header_line)
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
