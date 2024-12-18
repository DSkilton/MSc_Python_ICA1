"""
Main module for the Weather Data Application.

This module initializes and runs the WeatherDataApplication.
"""

# Author: <Duncan Skilton>
# Student ID: <S6310391>

import logging
from database_manager import DatabaseManager
from output_handler_registry import OutputHandlerRegistry
from console_output_handler import ConsoleOutputHandler
from graph_output_handler import GraphOutputHandler
from sqlite_query import SQLiteQuery
from menu_handler import MenuHandler

# TODO: Write tests for docstrings
# TODO: Write some integration tests
# TODO: Check all imports

# Register handlers dynamically
OutputHandlerRegistry.register_handler("console", ConsoleOutputHandler.handle_console)
OutputHandlerRegistry.register_handler("bar_chart", GraphOutputHandler.plot_bar)
OutputHandlerRegistry.register_handler("pie_chart", GraphOutputHandler.plot_pie)

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler() # Output to console
    ]
)
logging.getLogger('matplotlib').setLevel(logging.WARNING) # Changed log level because console was cluttered

class WeatherDataApplication:
    """
    Main application class for the Weather Data Application.

    Responsibilities:
    - Initializes database connection and query handlers.
    - Delegates user interactions to MenuHandler.
    - Manages application lifecycle.
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
        self.menu_handler = MenuHandler(self.query_instance, self.db_manager)
        self.logger.info("WeatherDataApplication initialised")


    def run(self):
        """
        Start application by repeatedly displaying the main menu
        until the user chooses to exit.
        """
        while True:
            choice = self.menu_handler.display_main_menu()

            try:
                if not self.menu_handler.handle_menu_choice(choice):
                    print("Exiting the application...")
                    break
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                print("An unexpected error occurred. Please try again.")


if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    # Initialize DatabaseManager and SQLiteQuery
    DB_PATH = r"db\CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    app = WeatherDataApplication(DB_PATH)
    app.run()
