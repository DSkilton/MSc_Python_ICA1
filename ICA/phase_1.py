# Author: <Duncan Skilton>
# Student ID: <S631>

import sqlite3
from DatabaseManager import DatabaseManager
from SQLiteQuery import SQLiteQuery
from Constants import SELECT_FROM, COUNTRIES_TBL, CITIES_TBL

# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.

'''
Satisfactory
'''

def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        # Define the query
        query = SELECT_FROM + COUNTRIES_TBL
        results = connection.execute_query(query=query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)


def select_all_cities(connection):
    try:
        query = SELECT_FROM + CITIES_TBL
        results = connection.execute_query(query=query)

        for result in results:
            print(f"City Id: {result['id']} -- City Name: {result['name']} -- Country Id: {result['country_id']}")

    except SQLiteQuery.OperationalError as e:
        print(e)
    

'''
Good
'''
def average_annual_temperature(city_id, year):
    SQLiteQuery.get_average_temperature(city_id=city_id, year=year)


def average_seven_day_precipitation(city_id, start_date):
    # TODO: Implement this function
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
    db_path = "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    db_manager = DatabaseManager(db_path)
    query_instance = SQLiteQuery(db_manager)
    
    select_all_countries(db_manager)
    select_all_cities(db_manager)

    db_manager.close_connection 

