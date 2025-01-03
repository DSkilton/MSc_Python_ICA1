"""
Menu Handler

Manages the user menu system for the Weather Data Application.
"""
import logging
from input_handler import InputHandler
from location_manager import LocationManager
from output_handler import OutputHandler
from console_output_handler import ConsoleOutputHandler
from session_manager import SessionManager
from geocoding_api_service import GeocodingApiService
from constants import *

class MenuHandler:
    """
    Handles menu display and user choice delegation.
    """

    def __init__(self, query_instance, db_manager, session_manager: SessionManager):
        """
        Initialize the MenuHandler.

        Parameters
        ----------
        query_instance : SQLiteQuery
            Instance of SQLiteQuery for database interactions.
        db_manager : DatabaseManager
            Instance of DatabaseManager for database management.
        session_manager : SessionManager
            Instance of SessionManager for session handling.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.query_instance = query_instance
        self.db_manager = db_manager
        self.session_manager = session_manager
        self.geocoding_service = GeocodingApiService(self.session_manager)
        self.location_manager = LocationManager(self.session_manager, self.geocoding_service)


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
        OutputHandler.handle_output(1, results, TITLE_COUNTRIES, X_LABEL_COUNTRIES, Y_LABEL_COUNTRY_ID)


    def view_cities(self):
        """
        Fetch and display all cities from the database.
        """
        results = self.query_instance.get_all_cities()
        OutputHandler.handle_output(1, results, TITLE_CITIES, X_LABEL_COUNTRIES, Y_LABEL_COUNTRY_ID)


    def average_annual_temperature(self):
        """
        Retrieve and display the average annual temperature for a city in a given year.
        """
        location_name = input("Enter location name: ")
        if not location_name:
            print("Location name cannot be empty. Please enter a valid city name.")
            return
        year = InputHandler.get_year_input("Enter year as YYYY: ")

        start_date = f"{year}{START_OF_YEAR}"
        end_date = f"{year}{END_OF_YEAR}"
        self.session_manager.log_session_details()

        city_data = self.location_manager.ensure_location_in_database(location_name)
        self.session_manager.log_session_details()

        if isinstance(city_data, list) and len(city_data) > 0:
            city_id = city_data[0].id
        else:
            city_id = city_data.id

        self.logger.debug(f"menu_handler, after id")

        weather_data = self.location_manager.fetch_location_weather_data(city_data, start_date, end_date)
        self.logger.debug(f"menu_handler, weather data: {weather_data[:5]}")

        result = self.query_instance.get_average_temperature(city_id=city_id, year=year)
        # self.logger.debug(f"menu_handler, weather results: {result}")

        monthly_data = self.query_instance.get_monthly_average_temperature(weather_data)
        self.logger.debug(f"menu_handler, monthly data: {monthly_data} type: {type(monthly_data)}")

        self.delegate_output(monthly_data, title=TITLE_AVG_TEMP, xlabel=X_LABEL_YEAR, ylabel=Y_LABEL_TEMPERATURE)
        # ConsoleOutputHandler.handle_console(weather_data, result_title="Average Annual Temperature")


    def average_seven_day_precipitation(self):
        """
        Retrieve and display the average precipitation over a seven-day period for a city.
        """
        # Prompt user for city input
        city_input = input("Enter city ID or name: ")

        # Determine whether the input is an ID or a name
        if city_input.isdigit():
            # Search by city ID
            city_id = int(city_input)
        else:
            # Search by city name
            city = self.query_instance.get_city_by_name(city_input)
            if not city:
                print(f"City '{city_input}' not found.")
                return
            city_id = city.id

        # Get the start date
        start_date = InputHandler.get_date_input("Enter start date (yyyy-mm-dd): ")

        # Query the database for the average seven-day precipitation
        results = self.query_instance.average_seven_day_precipitation(city_id, start_date)

        # Display the results
        self.delegate_output(results, title=TITLE_7DAY_PRECIP, xlabel=X_LABEL_CITIES, ylabel=Y_LABEL_PRECIPITATION)


    def average_mean_temp_by_city(self):
        """
        Retrieve and display the mean temperature for a city over a specified date range.
        """
        date_from = InputHandler.get_date_input("Enter start date: ")
        date_to = InputHandler.get_date_input("Enter end date: ")
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        results = self.query_instance.average_mean_temp_by_city(date_from, date_to, city_id)
        self.delegate_output(results, title=TITLE_MEAN_TEMP_CITY, xlabel=X_LABEL_TEMPERATURE, ylabel=Y_LABEL_TEMPERATURE)


    def average_annual_precipitation_by_country(self):
        """
        Retrieve and display the annual precipitation for all cities in a given country.
        """
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        country_id = InputHandler.get_integer_input("Enter country ID: ")
        results = self.query_instance.average_annual_preciption_by_country(country_id, year)
        self.delegate_output(results, title=TITLE_ANNUAL_PRECIP, xlabel=X_LABEL_PRECIPITATION, ylabel=Y_LABEL_PRECIPITATION)


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
        self.logger.debug(f"delegating output")
        print("How would you like to display the data?")
        print("1. Console")
        print("2. Bar Chart")
        print("3. Pie Chart")
        choice = InputHandler.get_integer_input("Enter your choice: ")

        self.logger.debug(f"User selected display option: {choice}")
        self.logger.debug(f"Graph details: {title, xlabel, ylabel}")
        self.logger.debug(f"Results being passed: {results}")

        OutputHandler.handle_output(choice, results, title, xlabel, ylabel)


    def exit_application(self):
            """
            Close the application and the database connection.
            """
            print("Closing application")
            self.db_manager.close_connection()
