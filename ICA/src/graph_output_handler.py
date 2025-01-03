import matplotlib.pyplot as plt
import logging

class GraphOutputHandler:
    """
    Handles graph plotting for various data visualization types.
    """

    logger = logging.getLogger(__name__)

    @staticmethod
    def handle_graph(choice, labels, values, title, xlabel=None, ylabel=None):
        """
        Routes the graph display based on user choice.

        Parameters
        ----------
        choice : str
            The type of graph to display ("bar_chart", "pie_chart", etc.).
        labels : list[str]
            A list of labels for the x-axis.
        values : list[int]
            A list of numerical values for the y-axis.
        title : str
            The title of the chart.
        xlabel : str, optional
            The label for the x-axis.
        ylabel : str, optional
            The label for the y-axis.
        """
        GraphOutputHandler.logger.info(f"Title: {title}, X-Label: {xlabel}, Y-Label: {ylabel}")
        GraphOutputHandler.logger.info(f"Graph type: {choice}")
        GraphOutputHandler.logger.info(f"Labels: {labels}")
        GraphOutputHandler.logger.info(f"Values: {values}")

        if not values or sum([v for v in values if isinstance(v, (int, float))]) == 0:
            GraphOutputHandler.logger.warning("No valid data for graphing.")
            print("No valid data available for graphing.")
            return

        # Filter out invalid values
        valid_data = [(label, value) for label, value in zip(labels, values) if isinstance(value, (int, float))]
        if not valid_data:
            GraphOutputHandler.logger.warning("No valid numeric data available for graphing.")
            print("No valid numeric data to display as a graph.")
            return

        # Unpack filtered data
        labels, values = zip(*valid_data)

        GraphOutputHandler.logger.debug(f"Filtered Labels: {labels}")
        GraphOutputHandler.logger.debug(f"Filtered Values: {values}")

        try:
            if choice == "bar_chart":
                GraphOutputHandler.plot_bar(labels, values, title, xlabel, ylabel)
            elif choice == "pie_chart":
                GraphOutputHandler.plot_pie(values, labels, title)
            else:
                print(f"Graph type '{choice}' is not supported.")
        except ValueError as e:
            GraphOutputHandler.logger.error(f"Graph rendering failed: {e}")
            print(f"Error: Unable to generate chart. {e}")
            print("Falling back to console output.")
            print("Results:", values)


    @staticmethod
    def plot_bar(labels: list[str], values: list[int], title: str, xlabel: str, ylabel: str):
        """
        Plot a bar chart using the given labels and values.

        Parameters
        ----------
        labels : list[str]
            A list of labels for the x-axis.
        values : list[int]
            A list of numerical values for the y-axis.
        title : str
            The title of the bar chart.
        xlabel : str
            The label for the x-axis.
        ylabel : str
            The label for the y-axis.
        """
        plt.close('all')

        GraphOutputHandler.logger.debug(f"plot bar, title: {title}")
        GraphOutputHandler.logger.debug(f"plot bar, xlabel: {xlabel}")
        GraphOutputHandler.logger.debug(f"plot bar, ylabel: {ylabel}")

        GraphOutputHandler.logger.debug(f"plot bar, Labels: {labels}")
        GraphOutputHandler.logger.debug(f"plot bar, Values: {values}")

        try:
            if not values or sum([v for v in values if isinstance(v, (int, float))]) == 0:
                GraphOutputHandler.logger.warning("No valid data for bar chart.")
                print("No valid data available for bar chart.")
                return

            plt.figure(figsize=(10, 6))
            plt.bar(labels, values)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            GraphOutputHandler.logger.error(f"Error plotting bar chart: {e}")
            print(f"Error generating chart: {e}. Falling back to console output.")
            GraphOutputHandler.logger.debug(f"Labels: {labels}, Values: {values}")


    @staticmethod
    def plot_pie(labels, values, title):
        """
        Plot a pie chart using the given labels and values.

        Parameters
        ----------
        values : list[int]
            A list of numerical values for the y-axis.
        labels : list[str]
            A list of labels for the x-axis.
        title : str
            The title of the bar chart.
        """
        plt.close('all')
        try:
            if not values or sum([v for v in values if isinstance(v, (int, float))]) == 0:
                GraphOutputHandler.logger.warning("No valid data for pie chart.")
                print("No valid data available for pie chart.")
                return

            values = [float(v) for v in values]
            plt.figure(figsize=(8, 8))
            plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
            plt.title(title)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            GraphOutputHandler.logger.error(f"Pie chart error: {e}")
            print("Failed to generate pie chart. Falling back to console.")


    @staticmethod
    def plot_scatter(labels, values, title, xlabel, ylabel):
        """
        Plot a scatter chart using the given labels and values.

        Parameters
        ----------
        labels : list[str]
            A list of labels for the x-axis.
        values : list[int]
            A list of numerical values for the y-axis.
        title : str
            The title of the bar chart.
        xlabel : str
            The label for the x-axis.
        ylabel : str
            The label for the y-axis.
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(labels, values, c='blue', marker='o')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()
        plt.show()