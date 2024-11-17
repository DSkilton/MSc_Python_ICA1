import sqlite3

class DatabaseManager: # a class to manage db operations
    def __init__(self, db_path: str):
        """
        Constructor to initialize a connection to the SQLite database.
        :param db_path: Path to the SQLite database file.
        """
        # TODO: ensure if db doesn't exist, appropriate message is returned rather than creating a new db
        self.connection = sqlite3.connect(db_path)


    def execute_query(self, query: str):
        """
        Executes an SQL query on the database.
        :param query: SQL query string.
        :param params: Tuple of parameters to safely inject into the query (default is an empty tuple).
        :return: The result of the query (a list of rows).
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchAll()
    
    
    def close_connection(self):
        """
        Closes the database connection.
        Ensures that the connection to the SQLite database is properly terminated.
        """
        self.connection.close()

