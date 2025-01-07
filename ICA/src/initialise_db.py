from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import logging
import os

def initialise_db(db_path: str):
    """
    Initialize the database, setting up the schema and ensuring the correct constraints.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()  # Output to console
        ]
    )
    logger = logging.getLogger("initialize_db")

    try:
        abs_db_path = db_path
        # Ensure the directory for the database exists
        db_directory = os.path.dirname(abs_db_path)
        if not os.path.exists(db_directory):
            raise FileNotFoundError(f"The directory for the database does not exist: {db_directory}")

        # Check if the file already exists and if it's writable
        if os.path.exists(abs_db_path) and not os.access(abs_db_path, os.W_OK):
            raise PermissionError(f"Cannot write to the database file: {abs_db_path}")

        # Create engine and connect to the SQLite database
        engine = create_engine(f"sqlite:///{abs_db_path}")
        print(f"engine: {engine}")

        # Create tables based on models
        logger.info("Creating tables...")
        Base.metadata.create_all(engine)
        logger.info("Tables created successfully.")

        # Open a session to verify insertion
        Session = sessionmaker(bind=engine)
        session = Session()
        session.close()

        logger.info("Database initialization completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during database initialization: {e}")


if __name__ == "__main__":
    DB_PATH = "db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    print("initialise_db db_path: {DB_PATH}")
    initialise_db(DB_PATH)
