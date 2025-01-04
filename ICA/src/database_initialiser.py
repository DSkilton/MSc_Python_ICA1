import threading
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


def remove_duplicates(session, model):
    """
    Remove duplicate rows from the given model, excluding the 'id' column.
    
    Parameters
    ----------
    session : Session
        The SQLAlchemy session object.
    model : Base
        The SQLAlchemy model class (Country, City, DailyWeatherEntry).
    """
    try:
        # Initialize an empty list to collect duplicates
        duplicates = []

        # Query the rows in the table excluding the 'id' column
        if model == Country:
            # Country has 'name' and 'timezone' as unique identifiers
            query = """
                WITH DuplicateRows AS (
                    SELECT 
                        name, 
                        timezone, 
                        MIN(ROWID) AS min_rowid -- Keep the first occurrence (row with the smallest ROWID)
                    FROM countries
                    GROUP BY name, timezone
                    HAVING COUNT(*) > 1
                )
                DELETE FROM countries
                WHERE ROWID NOT IN (
                    SELECT min_rowid
                    FROM DuplicateRows
                );
            """
            duplicates = session.execute(query).fetchall()

        elif model == City:
            # City has 'name', 'latitude', 'longitude', 'country_id' as unique identifiers
            query = """
                SELECT name, 
                ROUND(latitude, 6) AS latitude, 
                ROUND(longitude, 6) AS longitude, 
                country_id, 
                COUNT(*)
            FROM cities
            GROUP BY name, 
                    ROUND(latitude, 6), 
                    ROUND(longitude, 6), 
                    country_id
            HAVING COUNT(*) > 1;
            """
            duplicates = session.execute(query).fetchall()

        elif model == DailyWeatherEntry:
            # DailyWeatherEntry has 'date', 'city_id', 'max_temp', 'min_temp', 'precipitation' as unique identifiers
            query = """
                WITH DuplicateRows AS (
                    SELECT 
                        date, 
                        city_id, 
                        max_temp, 
                        min_temp, 
                        precipitation, 
                        MIN(ROWID) AS min_rowid -- Keep the first occurrence (row with the smallest ROWID)
                    FROM daily_weather_entries
                    GROUP BY date, city_id, max_temp, min_temp, precipitation
                    HAVING COUNT(*) > 1
                )
                DELETE FROM daily_weather_entries
                WHERE ROWID NOT IN (
                    SELECT min_rowid
                    FROM DuplicateRows
                );
            """
            duplicates = session.execute(query).fetchall()

        # Remove duplicates based on the results of the query
        for duplicate in duplicates:
            rowid = duplicate[-1]  # Get the ROWID of the earliest occurrence
            # Prepare the WHERE clause conditions for deleting duplicates, except for the MIN(ROWID)
            condition = " AND ".join([f"{column} = :{column}" for column in duplicate[:-1]])
            # Delete duplicate rows, keeping only the one with MIN(ROWID)
            session.execute(f"DELETE FROM {model.__tablename__} WHERE ROWID != {rowid} AND ({condition})",
                            {column: value for column, value in zip(duplicate[:-1], duplicate[:-1])})

        # Commit changes
        session.commit()
        logger.info(f"Duplicates removed for {model.__name__}")

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error during duplicate removal for {model.__name__}: {e}")
        raise


def clean_duplicates_in_background():
    """
    This function runs the cleanup process in a background thread.
    It will remove duplicates from all tables (Country, City, DailyWeatherEntry).
    """
    session = Session()

    try:
        # Run duplicate removal for each model in a background thread
        logger.info("Starting background cleanup of duplicate rows...")
        models = [Country, City, DailyWeatherEntry]
        for model in models:
            threading.Thread(target=remove_duplicates, args=(session, model), daemon=True).start()

    except SQLAlchemyError as e:
        logger.error(f"Error during cleanup process: {e}")
    finally:
        session.close()


def initialise_database():
    """
    Initializes the database by creating tables if they don't exist and cleaning duplicates.
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(engine)
        logger.info("Database initialised successfully.")

        # Start the cleanup process in the background
        clean_duplicates_in_background()

    except SQLAlchemyError as e:
        logger.error(f"Database initialisation failed: {e}")
        raise


if __name__ == "__main__":
    initialise_database()
