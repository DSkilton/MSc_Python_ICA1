import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import exists
from models.daily_weather_entry import DailyWeatherEntry
from models.city import City
from models.country import Country
from database_query_interface import DatabaseQueryInterface


class SQLiteQuery(DatabaseQueryInterface):
    """
    Handles predefined queries for weather-related data from an SQLAlchemy database.
    Implements DatabaseQueryInterface.
    """

    def __init__(self, session: Session):
        """
        Initialize SQLiteQuery with a database session.

        Parameters
        ----------
        session : Session
            SQLAlchemy session for database interactions.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = session


    def get_all_countries(self):
        """
        Retrieve all countries.

        Returns
        -------
        list[Country]
            All countries as SQLAlchemy objects.
        """
        return self.session.query(Country).all()


    def get_country_by_name(self, country_name):
        """
        Fetch a country by name.

        Parameters
        ----------
        country_name : str
            The country name.

        Returns
        -------
        Country or None
        """
        return self.session.query(Country).filter(Country.name == country_name).first()


    def get_country_by_id(self, country_name):
        """
        Fetch a country by name.

        Parameters
        ----------
        country_name : str
            The country name.

        Returns
        -------
        Country or None
        """
        return self.session.query(Country).filter(Country.name == country_name).first()


    def get_all_cities(self):
        """
        Retrieve all cities.

        Returns
        -------
        list[City]
        """
        return self.session.query(City).all()


    def get_average_temperature(self, city_id: int, year: int):
        """
        Calculate average temperature for a city in a given year.

        Parameters
        ----------
        city_id : int
            City ID.
        year : int
            Year.

        Returns
        -------
        float or None
        """
        # Log the city_id and year
        self.logger.debug(f"Received city_id: {city_id} (type: {type(city_id)}), year: {year} (type: {type(year)})")

        # Generate the start and end dates for the given year
        int_year = int(year)
        start_date = datetime(int_year, 1, 1)
        end_date = datetime(int_year, 12, 31)

        # Log the generated start and end dates with their types
        self.logger.debug(f"Generated start_date: {start_date} (type: {type(start_date)}), end_date: {end_date} (type: {type(end_date)})")

        # Query the database to get the average temperature
        avg_temp = (
            self.session.query(func.avg(DailyWeatherEntry.mean_temp))
            .filter(DailyWeatherEntry.city_id == city_id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .scalar()
        )

        # Log the result of the query and its type
        # self.logger.debug(f"Query result avg_temp: {avg_temp} (type: {type(avg_temp)})")

        # Check if the result is None and log accordingly
        if avg_temp is None:
            self.logger.warning(f"No average temperature found for city {city_id} in year {year}.")
        else:
            self.logger.debug(f"Average temperature: {avg_temp} found for city {city_id} in year {year}.")
        return avg_temp


    def get_precipitation_data(self, city_id: int, year: int):
        """
        Calculate total precipitation for a city in a given year.

        Parameters
        ----------
        city_id : int
            City ID.
        year : int
            Year.

        Returns
        -------
        float or None
        """
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        total_precip = (
            self.session.query(func.sum(DailyWeatherEntry.precipitation))
            .filter(DailyWeatherEntry.city_id == city_id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .scalar()
        )
        return total_precip


    def average_seven_day_precipitation(self, city_id, start_date):
        """
        Calculate average precipitation over seven days.

        Parameters
        ----------
        city_id : int
            City ID.
        start_date : str
            Start date.

        Returns
        -------
        float or None
        """
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = start_date + timedelta(days=6)

        avg_precip = (
            self.session.query(func.avg(DailyWeatherEntry.precipitation))
            .filter(DailyWeatherEntry.city_id == city_id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .scalar()
        )
        return avg_precip


    def average_mean_temp_by_city(self, city_id, start_date, end_date):
        """
        Calculate mean temperature for a city between two dates.

        Parameters
        ----------
        city_id : int
            City ID.
        start_date : str
            Start date.
        end_date : str
            End date.

        Returns
        -------
        float or None
        """
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        avg_temp = (
            self.session.query(func.avg(DailyWeatherEntry.mean_temp))
            .filter(DailyWeatherEntry.city_id == city_id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .scalar()
        )
        return avg_temp


    def average_annual_precipitation_by_country(self, country_id, year):
        """
        Calculate total precipitation for a country in a year.

        Parameters
        ----------
        country_id : int
            Country ID.
        year : int
            Year.

        Returns
        -------
        float or None
        """
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        total_precip = (
            self.session.query(func.sum(DailyWeatherEntry.precipitation))
            .join(City, City.id == DailyWeatherEntry.city_id)
            .filter(City.country_id == country_id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .scalar()
        )
        return total_precip


    def does_city_exist(self, city_name: str):
        """
        Check if a city exists in the database by its name using SQLAlchemy.

        Parameters
        ----------
        city_name : str
            The name of the city.
        session : Session
            The SQLAlchemy session.

        Returns
        -------
        bool
            True if the city exists, False otherwise.
        """
        exists_query = self.session.query(exists().where(City.name == city_name))
        return self.session.query(exists_query).scalar()


    def get_country_id_by_name(self, country_name: str):
        """
        Retrieve the country ID based on the country name using SQLAlchemy.

        Parameters
        ----------
        country_name : str
            The name of the country.
        session : Session
            The SQLAlchemy session.

        Returns
        -------
        int or None
            The ID of the country, or None if not found.
        """
        country = self.session.query(Country).filter(Country.name == country_name).first()
        return country.id if country else None


    def insert_city(self, city_data: dict):
        """
        Insert a new city into the database using SQLAlchemy.

        Parameters
        ----------
        city_data : dict
            Dictionary containing city information (name, latitude, longitude, country, timezone).
        """
        country_id = self.get_country_id_by_name(city_data['country'])
        if country_id is None:
            raise ValueError(f"Country '{city_data['country']}' not found in the database.")

        new_city = City(
            name=city_data['name'],
            latitude=city_data['latitude'],
            longitude=city_data['longitude'],
            country_id=country_id,
            timezone=city_data['timezone']
        )

        self.session.add(new_city)
        self.session.commit()
        self.session.refresh(new_city)
        return new_city
