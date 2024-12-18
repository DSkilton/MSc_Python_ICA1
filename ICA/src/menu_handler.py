"""
Menu Handler

Manages the user menu system for the Weather Data Application.
"""
import logging
from input_handler import InputHandler
from output_handler import OutputHandler
from database_manager import DatabaseManager
from constants import (
    MENU_VIEW_COUNTRIES, MENU_VIEW_CITIES, MENU_AVG_TEMP, MENU_7DAY_PRECIP,
    MENU_MEAN_TEMP_CITY, MENU_ANNUAL_PRECIP_CITY, MENU_EXIT,
    TITLE_COUNTRIES, TITLE_CITIES, TITLE_AVG_TEMP, TITLE_7DAY_PRECIP, TITLE_ANNUAL_PRECIP,
    X_LABEL_CITIES, X_LABEL_COUNTRIES, X_LABEL_YEAR, TITLE_MEAN_TEMP_CITY, X_LABEL_TEMPERATURE, 
    Y_LABEL_CITY_ID, Y_LABEL_COUNTRY_ID, Y_LABEL_TEMPERATURE, Y_LABEL_PRECIPITATION, X_LABEL_PRECIPITATION
)

class MenuHandler:
    """
    Handles menu display and user choice delegation.
    """

    def __init__(self, query_instance, db_manager):
        """
        Initialize the MenuHandler.

        Parameters
        ----------
        query_instance : SQLiteQuery
            Instance of SQLiteQuery for database interactions.
        """
        self.query_instance = query_instance
        self.db_manager = db_manager


    def display_main_menu(self):
        """
        Display the main menu and capture user input.

        Returns
        -------
        int
            The user's menu choice.
        """
        print("\nWeather Data Application")
        print("1. View all countries")
        print("2. View all cities")
        print("3. Get average annual temperature")
        print("4. Get seven-day precipitation")
        print("5. Get mean temperature by city")
        print("6. Get annual precipitation by country")
        print("0. Exit")
        return InputHandler.get_integer_input("Enter your choice: ")


    def handle_menu_choice(self, choice):
        """
        Handle the user's menu choice by delegating to the appropriate method.

        Parameters
        ----------
        choice : int
            The user's menu choice.
        """
        if choice == MENU_VIEW_COUNTRIES:
            self.view_countries()
        elif choice == MENU_VIEW_CITIES:
            self.view_cities()
        elif choice == MENU_AVG_TEMP:
            self.average_annual_temperature()  
        elif choice == MENU_7DAY_PRECIP:
            self.average_seven_day_precipitation()
        elif choice == MENU_MEAN_TEMP_CITY:
            self.average_mean_temp_by_city()
        elif choice == MENU_ANNUAL_PRECIP_CITY:
            self.average_annual_precipitation_by_country()
        elif choice == MENU_EXIT:
            return False
        else:
            print("Invalid choice, try again")
        return True


    def view_countries(self):
        """
        Fetch and display all countries from the database.
        """
        results = self.query_instance.get_all_countries()
        self.delegate_output(results, TITLE_COUNTRIES, X_LABEL_COUNTRIES, Y_LABEL_COUNTRY_ID)


    def view_cities(self):
        """
        Fetch and display all cities from the database.
        """
        results = self.query_instance.get_all_cities()
        self.delegate_output(results, TITLE_CITIES, X_LABEL_CITIES, Y_LABEL_CITY_ID)


    def average_annual_temperature(self):
        """
        Retrieve and display the average annual temperature for a city in a given year.

        Prompts the user to input a city ID and year, then queries the database for
        the average temperature and displays the result.
        """
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        results = self.query_instance.get_average_temperature(city_id=city_id, year=year)

        # self.logger.debug(f"results: {result}")
        self.delegate_output(results, title=TITLE_AVG_TEMP, xlabel=X_LABEL_YEAR, ylabel=Y_LABEL_TEMPERATURE)


    def average_seven_day_precipitation(self):
        """
        Retrieve and display the average precipitation over a seven-day period for a city.

        Prompts the user to input a city ID and start date, then calculates and displays 
        the average precipitation for the specified range.
        """
        city_id = InputHandler.get_integer_input("Enter city ID: ")
    
        start_date = InputHandler.get_date_input("Enter start date (yyyy-mm-dd): ")
        results = self.query_instance.average_seven_day_precipitation(city_id, start_date)

        self.delegate_output(results, title=TITLE_7DAY_PRECIP, xlabel=X_LABEL_PRECIPITATION, ylabel=Y_LABEL_PRECIPITATION)


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
        self.delegate_output(results, title=TITLE_MEAN_TEMP_CITY, xlabel=X_LABEL_TEMPERATURE, ylabel=Y_LABEL_TEMPERATURE)


    def average_annual_precipitation_by_country(self):
        """
        Retrieve and display the annual precipitation for all cities in a given country.

        Prompts the user to input a year and country ID, then sums the precipitation for
        all cities in that country and displays the result.
        """
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        country_id = InputHandler.get_integer_input("Enter country ID: ")
        results = self.query_instance.average_annual_preciption_by_country(country_id, year)

        self.delegate_output(results, title=TITLE_ANNUAL_PRECIP, xlabel=X_LABEL_PRECIPITATION, ylabel=Y_LABEL_PRECIPITATION)


    def select_all_countries(self):
        """
        Retrieve and display all countries from the database.

        Queries the `countries` table and presents the results in a user-specified format.
        """
        results = self.query_instance.select_all_countries()
        self.delegate_output(results, title=TITLE_COUNTRIES, xlabel=X_LABEL_COUNTRIES, ylabel=Y_LABEL_COUNTRY_ID)


    def select_all_cities(self):
        """
        Retrieve and display all cities from the database.

        Queries the `cities` table and presents the results in a user-specified format.
        """
        results = self.query_instance.execute_query()
        self.delegate_output(results, title=TITLE_CITIES, xlabel=X_LABEL_CITIES, ylabel=Y_LABEL_CITY_ID)


    def delegate_output(self, results, title, xlabel, ylabel):
        """
        Display query results using the OutputHandler.

        Parameters
        ----------
        results : list[dict]
            Query results to display.
        title : str
            Title for the output.
        xlabel : str
            Label for the x-axis (if applicable).
        ylabel : str
            Label for the y-axis (if applicable).
        """
        print("How would you like to display the data?")
        print("1. Console")
        print("2. Bar Chart")
        print("3. Pie Chart")
        choice = InputHandler.get_integer_input("Enter your choice: ")
        OutputHandler.handle_output(choice, results, title, xlabel, ylabel)


    def exit_application(self):
            """
            Close the application and the database connection.
            """
            print("Closing application")
            self.db_manager.close_connection()
            self.logger.info("Application closed.")