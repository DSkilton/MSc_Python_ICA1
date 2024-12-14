import matplotlib.pyplot as plt

class GraphHandler:
    """
    Handles graph plotting for various data visualization types.
    """

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