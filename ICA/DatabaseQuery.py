from abc import ABC, abstractmethod

class DatabaseQuery(ABC):
    @abstractmethod
    def get_average_temperature(self, city: str, year: int):
        """
        Abstract method to fetch average temp for a given city and year.
        Each data source will define its own logic. 
        """
        pass


    @abstractmethod
    def get_precipitation_data(self, city: str, year: int):
        """
        Abstract method to fetch precipitation data for a given city and year.
        Each data source will define its own logic. 
        """
        pass