from output_handler_registry import OutputHandlerRegistry

class OutputHandler:
    @staticmethod
    def handle_output(choice, results, title=None, xlabel=None, ylabel=None):
        """
        Delegates output handling based on the user's choice.

        Parameters
        ----------
        choice : int
            The display choice (i.e 1 for console, 2 for bar chart etc).
        results : list[dict]
            The data to display.
        title : str, optional
            The title for graphical outputs.
        xlabel : str, optional
            The x-axis label for graphical outputs.
        ylabel : str, optional
            The y-axis label for graphical outputs.
        """
        handlers = {
            1: "console",
            2: "bar_chart",
            3: "pie_chart"
        }
        handler_name = handlers.get(choice)
        handler = OutputHandlerRegistry.get_handler(handler_name)

        if handler:
            if handler_name == "console":
                handler(results)
            else:
                handler([row["name"] for row in results], [row["id"] for row in results], title, xlabel, ylabel)
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
        if not results:
            print("No results available")
            return
        
        # Determine the column headers based on the keys of the dictionary
        headers = results[0].keys()
        header_line = " | ".join(headers)
        print(header_line)
        print("-" * len(header_line))

        # Print each row of data
        for result in results:
            row_line = " | ".join(str(result[key]) for key in headers)
            print(row_line)