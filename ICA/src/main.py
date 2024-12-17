"""
Main module for the Weather Data Application.

This module initializes and runs the WeatherDataApplication.
"""

# Author: <Duncan Skilton>
# Student ID: <S6310391>
import sqlite3
import logging
from datetime import datetime
from input_handler import InputHandler
from constants import (
    SELECT_FROM, COUNTRIES_TBL, CITIES_TBL, MENU_VIEW_COUNTRIES, MENU_VIEW_CITIES, MENU_AVG_TEMP, 
    MENU_7DAY_PRECIP, MENU_MEAN_TEMP_CITY, MENU_ANNUAL_PRECIP_CITY, MENU_EXIT, TITLE_COUNTRIES, 
    TITLE_7DAY_PRECIP, TITLE_MEAN_TEMP_CITY, TITLE_ANNUAL_PRECIP, TITLE_AVG_TEMP, X_LABEL_PRECIPITATION, 
    X_LABEL_TEMPERATURE, Y_LABEL_CITY_ID, Y_LABEL_TEMPERATURE, Y_LABEL_PRECIPITATION, X_LABEL_YEAR,
    TITLE_CITIES, X_LABEL_CITIES, X_LABEL_COUNTRIES, Y_LABEL_COUNTRY_ID
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
# TODO: add data seperator - to constants
# TODO: Add DocString to database_query_interface

# Register handlers dynamically
OutputHandlerRegistry.register_handler("console", OutputHandler.handle_console)
OutputHandlerRegistry.register_handler("bar_chart", GraphHandler.plot_bar)
OutputHandlerRegistry.register_handler("pie_chart", GraphHandler.plot_pie)

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler() #output to console
    ]
)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

class WeatherDataApplication:
    """
    Main application class for the Weather Data Application.

    This class handles user interaction through a menu-driven interface, executes 
    database queries via the `SQLiteQuery` class, and displays results using the 
    `OutputHandler`.

    Attributes
    ----------
    db_manager : DatabaseManager
        Manages the SQLite database connection and queries.
    query_instance : SQLiteQuery
        Performs predefined weather-related queries on the database.
    """

    def __init__(self, db_path: str):
        """
        Initialize the WeatherDataApplication.

        Parameters
        ----------
        db_path : str
            The path to the SQLite database file.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_manager = DatabaseManager(db_path)
        self.query_instance = SQLiteQuery(self.db_manager)
        self.logger.info("WeatherDataApplication initialised")


    def validate_results(self, results):
        """
        Validate query results to ensure they contain data.

        Parameters
        ----------
        results : list, float, or None
            Query results from the database. Can be a list of rows, a numeric value, or None.

        Returns
        -------
        bool
            True if results are valid and contain data; otherwise, False.

        Notes
        -----
        - Numeric results are displayed directly.
        - Lists are checked to ensure they are iterable and contain valid rows.
        """
        # self.logger.debug(f"Validating results: {results}")

        if results is None:
            self.logger.warning(f"No data available.")
            print("No data found. Returning to the main menu...")
            return False

        # Handle numeric results
        if isinstance(results, (int, float)):
            OutputHandler._display_single_result(results)
            return True
        
        # Check if results are iterable and if rows are accessible
        if isinstance(results, list):
            if all(isinstance(row, sqlite3.Row) for row in results):
                return True

        # print results to console
        if results:
            OutputHandler.handle_console(results)
            return True

        else:
            self.logger.error(f"Invalid data format in results")
            print("Invalid data format. Returning to the main menu...")
            return False


    def run(self):
        """
        Display the main console menu and handle user interaction.

        Presents a menu of options to the user for querying weather data and
        selecting output formats. Each option triggers the corresponding query
        and display logic.

        The menu continues to loop until the user chooses to exit.
        """
        self.logger.info("Application started")
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

            try:
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
                    self.logger.warning(f"Invalid choice: {choice}")
                    print("Invalid choice, try again")
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                print(f"An error occurred: {e}. Returning to the main menu...")


    def exit_application(self):
        """
        Close the application and the database connection.
        """
        print("Closing application")
        self.db_manager.close_connection()


    def get_display_choice(self):
        """
        Prompt the user to choose a display format for query results.

        Returns
        -------
        int
            The user's chosen display format (e.g., 1 for console, 2 for bar chart).
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
        Retrieve and display all countries from the database.

        Queries the `countries` table and presents the results in a user-specified format.
        """
        query = SELECT_FROM + COUNTRIES_TBL
        results = self.db_manager.execute_query(query=query)

        if not self.validate_results(results):
            return

        choice = self.get_display_choice()
        OutputHandler.handle_output(choice, results, title=TITLE_COUNTRIES, xlabel=X_LABEL_COUNTRIES, ylabel=Y_LABEL_COUNTRY_ID)


    def select_all_cities(self):
        """
        Retrieve and display all cities from the database.

        Queries the `cities` table and presents the results in a user-specified format.
        """
        query = SELECT_FROM + CITIES_TBL
        results = self.db_manager.execute_query(query=query)

        if not self.validate_results(results):
            return

        choice = self.get_display_choice()
        OutputHandler.handle_output(choice, results, title=TITLE_CITIES, xlabel=X_LABEL_CITIES, ylabel=Y_LABEL_CITY_ID)


    def average_annual_temperature(self):
        """
        Retrieve and display the average annual temperature for a city in a given year.

        Prompts the user to input a city ID and year, then queries the database for
        the average temperature and displays the result.
        """
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        result = self.query_instance.get_average_temperature(city_id=city_id, year=year)

        # self.logger.debug(f"results: {result}")
        if not self.validate_results([result]):
            return

        choice = self.get_display_choice()
        OutputHandler.handle_output(choice, result, title=TITLE_AVG_TEMP, xlabel=X_LABEL_YEAR, ylabel=Y_LABEL_TEMPERATURE)


    def average_seven_day_precipitation(self):
        """
        Retrieve and display the average precipitation over a seven-day period for a city.

        Prompts the user to input a city ID and start date, then calculates and displays 
        the average precipitation for the specified range.
        """
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        while True:
            start_date = InputHandler.get_date_input("Enter start date (yyyy-mm-dd): ")
            results = self.query_instance.average_seven_day_precipitation(city_id, start_date)

            if not self.validate_results(results):
                return  # Exit gracefully to the main menu

            choice = self.get_display_choice()
            OutputHandler.handle_output(choice, results, title=TITLE_7DAY_PRECIP, xlabel=X_LABEL_PRECIPITATION, ylabel=Y_LABEL_PRECIPITATION)
            break


    def average_mean_temp_by_city(self):
        """
        Retrieve and display the mean temperature for a city over a specified date range.

        Prompts the user for a start date, end date, and city ID, then queries the database 
        and displays the mean temperature result.
        """
        date_from = InputHandler.get_date_input("Enter start date: ")
        date_to = InputHandler.get_date_input("Enter end date: ")
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        results = self.query_instance.average_mean_temp_by_city(date_from, date_to, city_id)

        if not self.validate_results([results]):
            return

        choice = self.get_display_choice()
        OutputHandler.handle_output(choice, results, title=TITLE_MEAN_TEMP_CITY, xlabel=X_LABEL_TEMPERATURE, ylabel=Y_LABEL_TEMPERATURE)


    def average_annual_precipitation_by_country(self):
        """
        Retrieve and display the annual precipitation for all cities in a given country.

        Prompts the user to input a year and country ID, then sums the precipitation for
        all cities in that country and displays the result.
        """
        year = InputHandler.get_year_input("Enter year as YYYY: ")
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
    DB_PATH = r"db\CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    app = WeatherDataApplication(DB_PATH)
    app.run()
