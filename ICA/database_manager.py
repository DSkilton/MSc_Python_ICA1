import sqlite3
import os

class DatabaseManager: # a class to manage db operations
    def __init__(self, db_path: str):
        """
        Constructor to initialize a connection to the SQLite database.
        :param db_path: Path to the SQLite database file.
        :raises FileNotFoundError: if the database does not exist
        """
        resolved_path = os.path.abspath(db_path)  # Get the absolute path of the database
        print(f"Resolved Database Path: {resolved_path}")  # Debugging statement
        if not os.path.exists(resolved_path):
            raise FileNotFoundError(f"Database not found at location: {resolved_path}")
        self.connection = sqlite3.connect(resolved_path)


    def execute_query(self, query: str, params: tuple=()):
        """
        Executes an SQL query on the database.
        :param query: SQL query string.
        :param params: Tuple of parameters for the SQL query.
        :return: The result of the query (a list of rows).
        """
        cursor = self.connection.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(query, params)
        return cursor.fetchall()
    
    
    def close_connection(self):
        """
        Closes the database connection.
        Ensures that the connection to the SQLite database is properly terminated.
        """
        self.connection.close()

