import logging
import os
import sqlite3


# TODO: Add doc string at class level and method level

class DatabaseManager:
    """
    Manages SQLite database operations.

    This class provides methods for executing queries and managing the connection
    to an SQLite database.
    """


    def __init__(self, db_path: str):
        """
        Initialize the DatabaseManager with a connection to the SQLite database.

        Parameters
        ----------
        db_path : str
            Path to the SQLite database file.

        Raises
        ------
        FileNotFoundError
            If the specified database file does not exist.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        if not os.path.exists(db_path):
            self.logger.critical(f"Database not found at location: {db_path}")
            raise FileNotFoundError(f"Database not found at location: {db_path}")
        self.logger.info(f"Connected to database at: {db_path}")
        self.connection = sqlite3.connect(db_path)


    def execute_query(self, query: str, params: tuple=()):
        """
        Execute an SQL query on the database.

        Parameters
        ----------
        query : str
            The SQL query string to execute.
        params : tuple, optional
            A tuple of parameters to bind to the SQL query. Defaults to an empty tuple.

        Returns
        -------
        list
            A list of rows returned by the query, where each row is a dictionary-like object.

        Raises
        ------
        sqlite3.OperationalError
            If the query is invalid or fails to execute.
        """
        self.logger.debug(f"DB MAN - Executing Query: {query} | Params: {params}")

        if params is None:
            params = ()

        try: 
            cursor = self.connection.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except sqlite3.OperationalError as e:
            self.logger.error(f"Database query failed: {e}")
            return []


    def close_connection(self):
        """
        Close the connection to the SQLite database.

        This ensures that any pending transactions are committed
        and the connection is properly terminated.
        """
        self.logger.info("Closing database connection")
        self.connection.close()
