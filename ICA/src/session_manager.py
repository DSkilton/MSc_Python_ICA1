import logging
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class SessionManager:
    """
    Manages SQLAlchemy sessions using the Singleton pattern
    Ensures that only one instance of the session exists during the application's lifecycle.
    """
    logger = logging.getLogger(__name__)

    _instance = None

    def __new__(cls, db_session_factory):
        """
        Ensures that only one instance of the SessionManager is created.
        """
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.db_session_factory = db_session_factory
            cls._instance.logger = logging.getLogger(__name__)
        return cls._instance


    def get_session(self):
        """
        Returns the session from the session factory.
        If a session has already been created, returns the existing session.
        """
        if not hasattr(self, 'session'):
            self.session = self.db_session_factory()
            self.logger.debug("New session created.")
        return self.session


    def commit_session(self):
        """
        Commits the current session to the database.
        """
        try:
            self.logger.debug(f"Committing session: {id(self.session)}")
            self.session.commit()
            self.logger.debug(f"Session committed successfully: {id(self.session)}")
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Error during commit on session {id(self.session)}: {e}")


    def close_session(self):
        """
        Closes the current session.
        """
        if hasattr(self, 'session'):
            self.logger.debug(f"Closing session: {id(self.session)}")
            self.session.close()
            self.logger.debug(f"Session closed: {id(self.session)}")
            del self.session
        else:
            self.logger.warning("No session to close.")

    def log_session_details(self):
        """
        Logs detailed information about the current session's state.
        """
        if hasattr(self, 'session'):
            self.logger.debug(f"Session details: {id(self.session)}, Active: {self.session.is_active}, Transaction: {self.session.in_transaction()}")
        else:
            self.logger.warning("No active session to log.")