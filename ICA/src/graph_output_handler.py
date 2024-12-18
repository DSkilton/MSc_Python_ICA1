import matplotlib.pyplot as plt

class GraphOutputHandler:
    """
    Handles graph plotting for various data visualization types.
    """

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
        if choice == "bar_chart":
            GraphOutputHandler.plot_bar(labels, values, title, xlabel, ylabel)
        elif choice == "pie_chart":
            GraphOutputHandler.plot_pie(values, labels, title)
        elif choice == "scatter_plot":
            GraphOutputHandler.plot_scatter(labels, values, title, xlabel, ylabel)
        else:
            print(f"Graph type '{choice}' is not supported.")
        

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
        plt.bar(labels, values)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()



    @staticmethod
    def plot_pie(values, labels, title):
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
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title(title)
        plt.show()


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
        plt.scatter(labels, values)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()