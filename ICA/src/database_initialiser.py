from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Country, City, DailyWeatherEntry
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logger = logging.getLogger("db_initialiser")

# Database location
DATABASE_URL = "sqlite:///CIS4044-N-SDI-OPENMETEO-PARTIAL.db"

# Database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured Session class
Session = sessionmaker(bind=engine)


def initialise_database():
    """
    Initializes the database by creating tables if they don't exist.
    """

    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(engine)
        logger.info("Database initialised successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Database initialisation failed: {e}")
        raise

if __name__ == "__main__":
    initialise_database()