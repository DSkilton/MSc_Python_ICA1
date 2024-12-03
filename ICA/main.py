"""
Main module for the Weather Data Application.

This module initializes and runs the WeatherDataApplication.
"""

# Author: <Duncan Skilton>
# Student ID: <S6310391>

import os
from input_handler import InputHandler
from constants import SELECT_FROM, COUNTRIES_TBL, CITIES_TBL
from output_handler import OutputHandler
from ICA.sqlite_query import SQLiteQuery
from ICA.database_manager import DatabaseManager

# TODO: Add doc string at class level and method level
# TODO: Test doc strings work e.g. print(method/class.__doc__)
# TODO: Check all imports


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


    def run(self):
        """
        Display the main console menu and handle user interaction.
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

            if choice == 1:
                self.select_all_countries()
            elif choice == 2:
                self.select_all_cities()
            elif choice == 3:
                self.average_annual_temperature()
            elif choice == 4:
                self.average_seven_day_precipitation()
            elif choice == 5:
                self.average_mean_temp_by_city()
            elif choice == 6:
                self.average_annual_precipitation_by_country()
            elif choice == 0:
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


    def select_all_countries(self):
        """
        Query the database and display all the countries 
        """
        query = SELECT_FROM + COUNTRIES_TBL
        results = self.db_manager.execute_query(query=query)

        # TODO: Move this to the output_handler
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")


    def select_all_cities(self):
        """
        Query the database and display all cities 
        """
        query = SELECT_FROM + CITIES_TBL
        results = self.db_manager.execute_query(query=query)

        # TODO: Move this to the output_handler
        for result in results:
            print(f"City Id: {result['id']} -- City Name: {result['name']} -- Country Id: {result['country_id']}")


    def average_annual_temperature(self):
        """
        Calculate and display the average annual temperature for a specified city and year.
        """
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        result = self.query_instance.get_average_temperature(city_id=city_id, date=year)
        # TODO: This is returning an empty list.
        print(f"Average temperature: {result if result else "No data available"} ")


    def average_seven_day_precipitation(self):
        """
        Calculate and display the seven-day precipitation total for a specified city and date range.
        """
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        result = self.query_instance.average_seven_day_precipitation(city_id, year)
        # TODO: Double check output, should it be something more appropriate
        print(f"Average: {OutputHandler.format_two_decimals(result)}")


    def average_mean_temp_by_city(self):
        """
        Calculate and display the mean temperature for a city over a specified date range.
        """
        date_from = InputHandler.get_integer_input("Enter start date: ")
        date_to = InputHandler.get_integer_input("Enter end date: ")
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        result = self.query_instance.average_mean_temp_by_city(date_from, date_to, city_id)
        # TODO: Check results against db to ensure accuracy
        print(f"Result: {result}")


    def average_annual_precipitation_by_country(self):
        """
        Calculate and display the average annual precipitation for a country in a specified year.
        """
        year = InputHandler.get_year_input("Enter year as YYYY: ")
        # TODO: This should be for a country not city
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        results = self.query_instance.average_annual_preciption_by_country(city_id, year)
        print(f"Result: {results} mm of rainfall")


if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    # Initialize DatabaseManager and SQLiteQuery
    DB_PATH = "..\db\CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    app = WeatherDataApplication(DB_PATH)
    app.run()
