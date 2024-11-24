# Author: <Duncan Skilton>
# Student ID: <S631>

import os
from ICA.database_manager import DatabaseManager
from input_handler import InputHandler
from ICA.sqlite_query import SQLiteQuery
from Constants import SELECT_FROM, COUNTRIES_TBL, CITIES_TBL

# Note: Display all real/float numbers to 2 decimal places.

class WeatherDataApplication:
    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)
        self.query_instance = SQLiteQuery(self.db_manager)

    def run(self):
        while True:
            print("Weather Data Application")
            print("1. View all countries")
            print("2. View all cities")
            print("3. Get average annual temperature")
            print("0. Exit")
            choice = InputHandler.get_integer_input("Enter your choice: ")

            if choice == 1:
                self.select_all_countries()
            elif choice == 2:
                self.select_all_cities()
            elif choice == 3:
                self.average_annual_temperature()
            elif choice == 0:
                self.exit_application()
                break
            else:
                print("Invalid choice, try again")


    def exit_application(self):
        print("Closing application")
        self.db_manager.close_connection()


    def select_all_countries(self):
        # Queries the database and selects all the countries 
        # stored in the countries table of the database.
        # The returned results are then printed to the 
        # console.
        
        query = SELECT_FROM + COUNTRIES_TBL
        results = self.db_manager.execute_query(query=query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

        
    def select_all_cities(self):    
        # Queries the database and selects all the cities 
        # stored in the cities table of the database.
        # The returned results are then printed to the 
        # console.
        query = SELECT_FROM + CITIES_TBL
        results = self.db_manager.execute_query(query=query)

        for result in results:
            print(f"City Id: {result['id']} -- City Name: {result['name']} -- Country Id: {result['country_id']}")

        
    '''
    Good
    '''
    def average_annual_temperature(self):
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        year = InputHandler.get_date_input("Enter year as YYYY: ")
        result = self.query_instance.get_average_temperature(city_id=city_id, date=year) 
        # TODO: This is returning an empty list.
        print(f"Average temperature: {result if result else "No data available"} ")
        

    def average_seven_day_precipitation(self):
        city_id = InputHandler.get_integer_input("Enter city ID: ")
        year = InputHandler.get_date_input("Enter year as YYYY: ")
        result = self.query_instance.average_seven_day_precipitation(city_id, year)
        pass

    '''
    Very good
    '''
    def average_mean_temp_by_city(connection, date_from, date_to):
        # TODO: Implement this function
        pass


    def average_annual_precipitation_by_country(connection, year):
        # TODO: Implement this function
        pass

    '''
    Excellent
    You have gone beyond the basic requirements for this aspect.
    '''

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    # Initialize DatabaseManager and SQLiteQuery
    db_path = "..\db\CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    app = WeatherDataApplication(db_path)
    app.run()

