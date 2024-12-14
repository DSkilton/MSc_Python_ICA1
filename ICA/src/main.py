"""
Main module for the Weather Data Application.

This module initializes and runs the WeatherDataApplication.
"""

# Author: <Duncan Skilton>
# Student ID: <S6310391>

from datetime import datetime
from input_handler import InputHandler
from constants import (
    SELECT_FROM, COUNTRIES_TBL, CITIES_TBL, DISPLAY_CONSOLE, DISPLAY_BAR_CHART,
    MENU_VIEW_COUNTRIES, MENU_VIEW_CITIES, MENU_AVG_TEMP, MENU_7DAY_PRECIP,
    MENU_MEAN_TEMP_CITY, MENU_ANNUAL_PRECIP_CITY, MENU_GRAPHS, MENU_EXIT
)
from output_handler import OutputHandler
from sqlite_query import SQLiteQuery
from database_manager import DatabaseManager
from output_handler_registry import OutputHandlerRegistry
from graph_handler import GraphHandler


# TODO: Add doc string at class level and method level
# TODO: Test doc strings work e.g. print(method/class.__doc__)
# TODO: Write some integration tests
# TODO: Check all imports
# TODO: User date inputs must be historic i.e. no future dates

# Register handlers dynamically
OutputHandlerRegistry.register_handler("console", OutputHandler.handle_console)
OutputHandlerRegistry.register_handler("bar_chart", GraphHandler.plot_bar)
OutputHandlerRegistry.register_handler("pie_chart", GraphHandler.plot_pie)


class WeatherDataApplication:
    """
    Main application class for the Weather Data Application.

    This class initializes the application, handles user interaction, and manages database queries.
    """

    def __init__(self, db_path: str):
        """
        Initialize the WeatherDataApplication.

        Parameters
        ----------
        db_path : str
            The path to the SQLite database file.
        """
        self.db_manager = DatabaseManager(db_path)
        self.query_instance = SQLiteQuery(self.db_manager)

    
    def validate_results(self, results):
        """
        Validate query results to ensure they contain data.

        Parameters
        ----------
        results : list[dict]
            Query results from the database.

        Returns
        -------
        bool
            True if results are valid, False otherwise. Prints an error message if results are empty.
        """
        if not results:
            print("No data available.")
            return False
        return True


    def run(self):
        """
        Display the main console menu and handle user interaction.

        Presents a menu of options to the user for querying weather data and
        selecting output formats. Each option triggers the corresponding query
        and display logic.

        The menu continues to loop until the user chooses to exit.
        """
        while True:
            print("Weather Data Application")
            print("1. View all countries")
            print("2. View all cities")
            print("3. Get average annual temperature")
            print("4. Get seven day precipitation")
            print("5. Avg mean temp by city")
            print('6. Average annual precipitation by city')
            print("0. Exit")
            choice = InputHandler.get_integer_input("Enter your choice: ")

            if choice == MENU_VIEW_COUNTRIES:
                self.select_all_countries()
            elif choice == MENU_VIEW_CITIES:
                self.select_all_cities()
            elif choice == MENU_AVG_TEMP:
                self.average_annual_temperature()
            elif choice == MENU_7DAY_PRECIP:
                self.average_seven_day_precipitation()
            elif choice == MENU_MEAN_TEMP_CITY:
                self.average_mean_temp_by_city()
            elif choice == MENU_ANNUAL_PRECIP_CITY:
                self.average_annual_precipitation_by_country()
            elif choice == MENU_EXIT:
                self.exit_application()
                break
            else:
                print("Invalid choice, try again")


    def exit_application(self):
        """
        Close the application and the database connection.
        """
        print("Closing application")
        self.db_manager.close_connection()


    def get_display_choice(self):
        """
        Display a submenu for choosing how to visualize the data.

        Returns
        -------
        str
            The user's choice of display type.
        """
        print("How would you like to display the data?")
        print("1. Console (text-based)")
        print("2. Bar Chart")
        print("3. Pie Chart")
        print("4. Scatter Plot")
        print("5. Line Chart")
        return InputHandler.get_integer_input("Enter your choice: ")


    def select_all_countries(self):
        """
        Query the database and display all the countries 
        """
        query = SELECT_FROM + COUNTRIES_TBL
        results = self.db_manager.execute_query(query=query)

        if not self.validate_results(results):
            return

        choice = self.get_display_choice()
        # TODO: Change these string literals to constants
        OutputHandler.handle_output(choice, results, title=TITLE_COUNTRIES, xlabel=X_LABEL_COUNTRY_NAME, ylabel=Y_LABEL_ID)


    def select_all_cities(self):
        """
        Query the database and display all cities 
        """
        query = SELECT_FROM + CITIES_TBL
        results = self.db_manager.execute_query(query=query)

        if not self.validate_results(results):
            return

        choice = self.get_display_choice()
        OutputHandler.handle_output(choice, results, title=TITLE_CITY, xlabel=X_LABEL_CITY_NAME, ylabel=Y_LABEL_CITY_ID)


    def average_annual_temperature(self):
        """
        Calculate and display the average annual temperature for a specified city and year.
        """
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        result = self.query_instance.get_average_temperature(city_id=city_id, date=year)

        if not self.validate_results([result]):  
            return

        choice = self.get_display_choice()
        OutputHandler.handle_output(choice, result, title=TITLE_AVG_TEMP, xlabel=X_LABEL_YEAR, ylabel=Y_LABEL_TEMP)


    def average_seven_day_precipitation(self):
        """
        Calculate and display the seven-day precipitation total for a specified city and date range.
        """
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        while True:
            start_date = InputHandler.get_date_input("Enter start date (dd/mm/yyyy): ")
            # Ensure the start date is historic
            parsed_date = datetime.strptime(start_date, "%d/%m/%Y")
            if parsed_date > datetime.now():
                print("The start date cannot be in the future. Please try again.")
                continue

            # Query database and display results
            results = self.query_instance.average_seven_day_precipitation(city_id, start_date)

            if not self.validate_results([results]):  
                return

            choice = self.get_display_choice()
            OutputHandler.handle_output(choice, results, title=TITLE_7DAY_PRECIP, xlabel=X_LABEL_PRECIPITATION, ylabel=Y_LABEL_PRECIPITATION)


    def average_mean_temp_by_city(self):
        """
        Calculate and display the mean temperature for a city over a specified date range.
        """
        date_from = InputHandler.get_integer_input("Enter start date: ")
        date_to = InputHandler.get_integer_input("Enter end date: ")
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        results = self.query_instance.average_mean_temp_by_city(date_from, date_to, city_id)

        if not self.validate_results([results]):
            return

        choice = self.get_display_choice()
        OutputHandler.handle_output(choice, results, title=TITLE_MEAN_TEMP_CITY, xlabel=X_LABEL_TEMPERATURE, ylabel=Y_LABEL_TEMPERATURE)


    def average_annual_precipitation_by_country(self):
        """
        Calculate and display the average annual precipitation for a country in a specified year.
        """
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        # TODO: This should be for a country not city
        country_id = InputHandler.get_integer_input("Enter country ID: ")
        results = self.query_instance.average_annual_preciption_by_country(country_id, year)

        if not self.validate_results([results]):
            return
        
        choice = self.get_display_choice()
        OutputHandler.handle_output(choice, results, title=TITLE_ANNUAL_PRECIP, xlabel=X_LABEL_PRECIPITATION, ylabel=Y_LABEL_PRECIPITATION)


if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    # Initialize DatabaseManager and SQLiteQuery
    DB_PATH = "db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    app = WeatherDataApplication(DB_PATH)
    app.run()
