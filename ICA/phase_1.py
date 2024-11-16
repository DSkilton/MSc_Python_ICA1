# Author: <Duncan Skilton>
# Student ID: <S631>

import sqlite3


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
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)

def select_all_cities(connection):
    # TODO: Implement this function
    pass

'''
Good
'''
def average_annual_temperature(connection, city_id, year):
    # TODO: Implement this function
    pass

def average_seven_day_precipitation(connection, city_id, start_date):
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
    pass