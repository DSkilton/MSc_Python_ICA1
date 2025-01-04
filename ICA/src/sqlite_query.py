import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import exists
from models.daily_weather_entry import DailyWeatherEntry
from models.city import City
from models.country import Country
from database_query_interface import DatabaseQueryInterface
from collections import defaultdict



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


    def average_seven_day_precipitation(self, city_name, start_date):
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

        city = self.session.query(City).filter(City.name.ilike(city_name)).first()

        avg_precip = (
            self.session.query(DailyWeatherEntry.date, DailyWeatherEntry.precipitation)
            .filter(DailyWeatherEntry.city_id == city.id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .all()
        )
        precip_data = [(entry[0], entry[1]) for entry in avg_precip]
        self.logger.debug(f"7 day precip: {precip_data}")
        return precip_data


    def average_temp_by_city(self, start_date, end_date, city_name):
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
        self.logger.debug(f"Received city: {city_name}, start_date: {start_date}, end_date: {end_date})")

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        city = self.session.query(City).filter(City.name.ilike(city_name)).first()

        if not city:
            self.logger.error(f"City '{city_name}' not found in the database.")
            return None

        self.logger.debug(f"Fetched city: {city.name} with ID: {city.id}")

        # Query the average temperature for the given city and date range
        avg_temp = (
            self.session.query(func.avg(DailyWeatherEntry.mean_temp))
            .filter(DailyWeatherEntry.city_id == city.id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .scalar()
        )

        self.logger.debug(f"Average temperature for {city_name} from {start_date} to {end_date}: {avg_temp} °C")

        return avg_temp



    def average_annual_precipitation_by_country(self, country_name, year):
        """
        Calculate total precipitation for a country in a given year and return monthly totals.

        Parameters
        ----------
        country_name : str
            Name of the country.
        year : int
            Year.

        Returns
        -------
        dict
            A dictionary containing the total annual precipitation and a breakdown by month.
        """
        # Retrieve the country
        country = self.session.query(Country).filter(Country.name.ilike(country_name)).first()

        if not country:
            self.logger.error(f"Country '{country_name}' not found in the database.")
            return None

        # Define the start and end dates for the year
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        self.logger.debug(f"Received country: {country.name}, start_date: {start_date}, end_date: {end_date})")

        # Query for monthly precipitation totals per city in the country
        monthly_precip = (
            self.session.query(
                func.extract('month', DailyWeatherEntry.date).label('month'),
                func.sum(DailyWeatherEntry.precipitation).label('monthly_precip')
            )
            .join(City, City.id == DailyWeatherEntry.city_id)
            .join(Country, Country.id == City.country_id)
            .filter(Country.id == country.id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .group_by('month')
            .order_by('month')
            .all()
        )

        # Aggregate the data into a dictionary for monthly precipitation
        monthly_data = {month: round(precip, 2) for month, precip in monthly_precip}

        # Query for total precipitation for the year
        total_precip = (
            self.session.query(func.sum(DailyWeatherEntry.precipitation))
            .join(City, City.id == DailyWeatherEntry.city_id)
            .join(Country, Country.id == City.country_id)
            .filter(Country.id == country.id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .scalar()
        )

        total_precip = round(total_precip, 2) if total_precip is not None else 0

        self.logger.debug(f"Total precipitation for {country_name} in {year}: {total_precip} mm")

        # Return both the total annual precipitation and the monthly breakdown
        return {
            'total_precipitation': total_precip,
            'monthly_precipitation': monthly_data
        }


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


    def get_monthly_average_temperature(self, daily_weather_entries):
        """
        Calculate the average temperature for each month.
        
        Parameters
        ----------
        daily_weather_entries : list
            List of DailyWeatherEntry objects containing daily temperatures and dates.
        
        Returns
        -------
        dict
            A dictionary with months as keys and average temperatures as values.
        """
        monthly_data = defaultdict(list)

        for entry in daily_weather_entries:
            month = entry.date.month
            monthly_data[month].append(entry.mean_temp)

        # Calculate average temperature for each month
        monthly_avg_temp = {month: sum(temps)/len(temps) for month, temps in monthly_data.items()}

        return monthly_avg_temp