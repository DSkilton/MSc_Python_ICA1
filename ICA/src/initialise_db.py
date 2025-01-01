from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from os.path import abspath
import logging

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
        abs_db_path = abspath(db_path)
        engine = create_engine(f"sqlite:///{abs_db_path}")

        # Create tables based on models, but no unique constraint on latitude, longitude
        logger.info("Creating tables...")
        Base.metadata.create_all(engine)
        logger.info("Tables created successfully.")

        # Open a session to verify insertion
        Session = sessionmaker(bind=engine)
        session = Session()

        # Additional logic for any data setup can go here
        # For example, adding initial data or validating the schema

        # Example check for existing cities (optional)
        from models.city import City
        from models.country import Country
        example_city = City(name="Test City", latitude=10.0, longitude=20.0, timezone="UTC", country_id=1)
        session.add(example_city)
        session.commit()
        logger.info(f"Test city added with ID: {example_city.id}")

        session.close()
        logger.info("Database initialization completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during database initialization: {e}")

if __name__ == "__main__":
    DB_PATH = "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    initialize_db(DB_PATH)