import logging
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    """
    Manages database connection and session handling.
    """

    def __init__(self, engine):
        """
        Initialize the database manager with the provided database URL.

        Parameters
        ----------
        db_url : str
            The URL for the database connection.
        """
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)


    def get_session(self):
        """
        Create and return a new database session.

        Returns
        -------
        session : sqlalchemy.orm.Session
            A new database session instance.
        """
        return self.session()


    def close_session(self, session):
        """
        Close the given database session.

        Parameters
        ----------
        session : sqlalchemy.orm.Session
            The database session to close.
        """
        try:
            session.close()
        except Exception as e:
            print(f"Error closing session: {e}")


    def execute_query(self, query):
        """
        Execute a raw SQL query.

        Parameters
        ----------
        query : str
            The SQL query string to execute.

        Returns
        -------
        result : list
            A list of results from the query execution.
        """
        self.logger.debug(f"Executing query: {query}")
        session = self.get_session()
        try:
            result = session.execute(query).fetchall()
            self.logger.debug(f"Query executed successfully, found {len(result)} rows.")
            return result
        except SQLAlchemyError as e:
            self.logger.error(f"SQL query failed: {e}")
            session.rollback()
            raise
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
        finally:
            self.close_session(session)
