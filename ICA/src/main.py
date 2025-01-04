"""
Main module for the Weather Data Application.

This module initializes and runs the WeatherDataApplication.
"""

# Author: <Duncan Skilton>
# Student ID: <S6310391>

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os.path import abspath
from initialise_db import initialise_db
from session_manager import SessionManager
from output_handler_registry import OutputHandlerRegistry
from console_output_handler import ConsoleOutputHandler
from graph_output_handler import GraphOutputHandler
from weather_api_service import WeatherApiService
from sqlite_query import SQLiteQuery
from menu_handler import MenuHandler
from database_manager import DatabaseManager

# TODO: Write tests for docstrings
# TODO: Write some integration tests
# TODO: Check all imports
# TODO: Sort automated tests
# TODO: Stop duplicates being saved in db
# TODO: Longitude and Latitude shouldn't be 2 decimal places 🤦🏼‍♂️

# Register handlers dynamically
OutputHandlerRegistry.register_handler("console", ConsoleOutputHandler.handle_console)
OutputHandlerRegistry.register_handler("bar_chart", GraphOutputHandler.plot_bar)
OutputHandlerRegistry.register_handler("pie_chart", GraphOutputHandler.plot_pie)
# OutputHandlerRegistry.register_handler("scatter_plot", GraphOutputHandler.plot_scatter)
# OutputHandlerRegistry.register_handler("line_chart", GraphOutputHandler.plot_line)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)
logger = logging.getLogger(__name__)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

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

        # Initialize SQLAlchemy engine and session
        abs_db_path = abspath(db_path)
        engine = create_engine(f"sqlite:///{abs_db_path}")
        session_factory = sessionmaker(bind=engine)
        self.session_manager = SessionManager(session_factory)

        initialise_db(db_path)

        self.db_manager = DatabaseManager(engine)
        self.query_instance = SQLiteQuery(self.session_manager.get_session())
        self.menu_handler = MenuHandler(self.query_instance, self.db_manager, self.session_manager)
        self.weather_service = WeatherApiService(session=self.session_manager.get_session())

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

        # Close session on exit
        self.session_manager.close_session()


if __name__ == "__main__":
    # Initialize database path
    DB_PATH = "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    app = WeatherDataApplication(DB_PATH)
    app.run()