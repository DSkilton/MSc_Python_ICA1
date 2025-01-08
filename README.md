Weather Data Application - README and User Instructions

Project Overview
The Weather Data Application is a Python-based weather analysis tool that retrieves, stores, and visualizes weather data using the Open-Meteo API. It supports viewing weather data in multiple formats such as tables, bar charts, and pie charts.

The application is built with a modular architecture leveraging SQLAlchemy for database interactions and Matplotlib for data visualization.

1. Installation
Clone or download the repository.
Ensure Python 3.8 or higher is installed.

Install required dependencies:
    pip install -r requirements.txt

Create the database:
    python src/initialise_db.py

2. Directory Structure
src/
  ├── base_api_service.py        # Handles API requests and retries.
  ├── console_output_handler.py  # Outputs data in table format.
  ├── constants.py               # Stores constant values.
  ├── database_initialiser.py    # Creates and initializes the database.
  ├── database_manager.py        # Manages database queries and connections.
  ├── database_query_interface.py# Abstract interface for query operations.
  ├── geocoding_api_service.py   # Fetches city data from Geocoding API.
  ├── graph_output_handler.py    # Handles visual output (graphs).
  ├── input_handler.py           # Validates and processes user inputs.
  ├── location_manager.py        # Ensures location data exists in the database.
  ├── main.py                    # Entry point for the application.
  ├── menu_handler.py            # Handles menu interactions and processing.
  ├── models/                    # Database models (City, Country, WeatherEntry).
  ├── output_handler.py          # Delegates output to specific handlers.
  ├── output_handler_registry.py # Registers output handlers.
  ├── results_validator.py       # Validates query results.
  ├── session_manager.py         # Manages database sessions.
  ├── sqlite_query.py            # Executes database queries.
  ├── weather_api_service.py     # Fetches weather data via API.
  ├── weather_data.py            # Maps weather data into database models.
  ├── __init__.py                # Module initialization.

3. Configuration
The database is initialized in the db folder and is referenced in initialise_db.py:
    DB_PATH = "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"

4. Usage Instructions
4.1. Launch Application:
    python main.py

4.2. Main Menu
Upon launching, the following menu options are displayed:

    1. View all countries - Lists all countries stored in the database.
    2. View all cities - Lists all cities stored in the database.
    3. Get average annual temperature - Displays the average temperature for a specific city and year.
    4. Get seven-day precipitation - Fetches and displays precipitation data for 7 days starting from a specific date.
    5. Get mean temperature by city - Displays the mean temperature for a city between two specified dates.
    6. Get annual precipitation by country - Displays precipitation data grouped by month for a specific country and year.
    0. Exit - Closes the application.

4.3. Follow prompts to input required details:
    Location Name - Enter the name of the city or country.
    Year/Date Range - Provide year or start/end dates as prompted.
    Output Format - Choose between table (console) or graphical output (bar/pie charts).

5. Features
    API Integration:
    Fetches weather and geolocation data using Open-Meteo and Geocoding APIs.

    Database Management:
    Uses SQLite to store weather, city, and country data locally.

    Data Visualization:
    Generates bar and pie charts to visualize temperature and precipitation trends.

    Error Handling:
    Implements retry mechanisms for failed API requests and validates user inputs.

    Output Flexibility:
    Allows results to be displayed as tables or charts.

6. Error Handling
    Database Errors:

    Database initialization failures log errors and provide user-friendly messages.
    Duplicate records are handled in the background during database initialization.
    API Errors:

    Implements retries (default: 3 attempts) with delays for transient API issues.
    Logs errors for HTTP issues and invalid responses.
    Input Errors:

    Prompts users until valid inputs (numbers, dates, etc.) are provided.
    Graph Errors:

    Falls back to console output if a graph cannot be generated.

7. Troubleshooting
    Database Not Found:
    Ensure the db directory exists and has write permissions.
    
    Re-run database initialization:
        python src/initialise_db.py

    Missing Dependencies:
        Reinstall dependencies:
            pip install -r requirements.txt

    API Failures:
        Check internet connection and API availability.

    Logging Issues:
        View logs in the console for detailed error messages.

8. Dependencies
    Python 3.8 or higher
    SQLAlchemy - ORM for database management.
    Requests - Handles HTTP requests.
    Matplotlib - Generates charts for visual output.

    To install all dependencies:
        pip install -r requirements.txt