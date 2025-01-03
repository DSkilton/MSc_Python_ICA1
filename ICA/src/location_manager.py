import logging
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from weather_data import WeatherData
from weather_api_service import WeatherApiService
from session_manager import SessionManager
from geocoding_api_service import GeocodingApiService
from models import *
from constants import *

class LocationManager:
    """
    Manages location-related operations, including geocoding and database interactions.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, session_manager: SessionManager, geocoding_service: GeocodingApiService):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session_manager = session_manager
        self.db_session = session_manager.get_session()
        self.geocoding_service = geocoding_service
        self.weather_service = WeatherApiService(self.db_session)


    def ensure_location_in_database(self, location_name):
        """
        Ensures that a city with the given name exists in the database. If the city does not exist,
        it fetches the city data using the Geocoding API, creates a new country (if necessary), 
        and then adds the city to the database. If multiple cities are found, the user is prompted
        to select one.

        Parameters
        ----------
        location_name : str
            The name of the city to ensure exists in the database.

        Returns
        -------
        city : City
            The city object, either newly created or fetched from the database.
        """
        city_info = None
        self.session_manager.log_session_details()
        self.logger.debug(f"Starting transaction for '{location_name}'")

        # Check if the city already exists in the database
        self.logger.debug(f"Checking if city '{location_name}' exists in the database.")
        city = self.get_city_from_db(location_name)
        if city:
            self.logger.info(f"City '{location_name}' already exists in the database.")
            return [city]

        # Fetch the city data from the Geocoding API
        self.logger.debug(f"Fetching city data for '{location_name}' from Geocoding API.")
        location_data_list = self.geocoding_service.fetch_city_data(location_name)
        if len(location_data_list) > 1:
            # If multiple cities are found, prompt the user to select one
            self.logger.info(f"Multiple locations found for '{location_name}'. Please select one:")
            for idx, loc in enumerate(location_data_list):
                self.logger.debug(f"{idx + 1}. {loc.name}, {loc.country} (Lat: {loc.latitude}, Lon: {loc.longitude})")

            # Here, you'd have a method to handle user input. For simplicity, assume user selects the first city.
            choice = 0  # Assume user selected the first city for simplicity, replace with actual input handling
            city_info = location_data_list[choice]
            self.logger.debug(f"City info selected: {city_info}")
        else:
            city_info = location_data_list[0]
            self.logger.debug(f"Single city found: {city_info}")

        # Ensure the country exists in the database, or create it if it doesn't
        self.logger.debug(f"location, manager, Ensuring country '{city_info.country}' exists in the database.")
        country = self.ensure_country_exists(city_info.country_id)

        # Ensure the city exists, or create it if it doesn't
        self.logger.debug(f"Ensuring city '{city_info.name}' exists in the database.")
        city = self.ensure_city_exists(city_info.name, city_info.latitude, city_info.longitude, country)

        # Commit the transaction
        self.session_manager.commit_session()
        self.logger.info(f"Location '{location_name}' added to the database.")

        self.logger.debug(f"This is the return value: {city}")
        return [city]


    def ensure_country_exists(self, country_name):
        """
        Ensures that a country with the given name exists in the database.
        If the country does not exist, it creates a new country.

        Parameters:
        ----------
        country_name : str
            The name of the country to ensure exists in the database.

        Returns
        -------
        country : Country
            The Country object, either newly created or fetched from the database.
        """
        # Check if the country already exists in the database
        country = self.db_session.query(Country).filter_by(name=country_name).first()
        if not country:
            # If the country doesn't exist, create a new country
            self.logger.debug(f"Country '{country_name}' not found, creating new entry.")
            country = Country(name=country_name, timezone="Unavailable")  # Default timezone
            self.db_session.add(country)
            self.session_manager.commit_session()
            self.logger.info(f"Country '{country_name}' added to the database.")
        else:
            self.logger.debug(f"Country '{country_name}' already exists in the database.")

        return country


    def ensure_city_exists(self, city_name, latitude, longitude, country):
        """
        Ensures that a city with the given name, latitude, and longitude exists in the database.
        If the city does not exist, it creates a new city and associates it with the provided country.

        Parameters:
        ----------
        city_name : str
            The name of the city to ensure exists in the database.
        latitude : float
            The latitude of the city.
        longitude : float
            The longitude of the city.
        country : Country
            The Country object to associate the city with.

        Returns
        -------
        city : City
            The City object, either newly created or fetched from the database.
        """
        # Check if the city already exists in the database
        city = self.db_session.query(City).filter_by(name=city_name).first()

        if not city:
            # If city doesn't exist, create a new city and associate it with the country
            self.logger.debug(f"City '{city_name}' not found, creating new entry.")
            city = City(name=city_name, latitude=latitude, longitude=longitude, timezone="Unavailable", country_id=country.id)
            self.db_session.add(city)
            self.session_manager.commit_session()
            self.logger.info(f"City '{city_name}' added to the database with ID {city.id}.")
        else:
            self.logger.debug(f"City '{city_name}' already exists in the database.")

        return city


    def get_city_from_db(self, location_name):
        """
        Check if the city already exists in the database.

        Parameters
        ----------
        location_name : str
            Name of the city to check.

        Returns
        -------
        City or None
            The city if found, otherwise None.
        """
        self.logger.debug(f"Checking if location '{location_name}' exists in the database.")
        return self.db_session.query(City).options(joinedload(City.country)).filter_by(name=location_name).first()


    def fetch_location_weather_data(self, city_data, start_date, end_date):
        """
        Fetch historical weather data for a location.

        Parameters
        ----------
        location_name : str
            Name of the location to fetch weather data for.
        start_date : str
            Start date for the weather data (format: yyyy-mm-dd).
        end_date : str
            End date for the weather data (format: yyyy-mm-dd).

        Returns
        -------
        dict
            Weather data fetched for the location.
        """
        self.logger.debug(f"Checking if location '{city_data}' exists in the database.")

        # Get the city from the data
        city = self.get_city_from_data(city_data)

        if not city:
            self.logger.error(f"City '{city_data}' not found in the database.")
            return {}

        # Fetch weather data for the city
        weather_data = self.fetch_weather_data_for_city(city, start_date, end_date)

        if not weather_data:
            self.logger.error(f"Failed to fetch valid weather data for city '{city.name}'.")
            return {}

        # Process and store the weather data
        return self.process_weather_data(weather_data, city)


    def get_city_from_data(self, city_data):
        """
        Extracts the city object from the provided city data.

        Parameters
        ----------
        city_data : list or City
            City data which can either be a list (if multiple cities) or a single city object.

        Returns
        -------
        City or None
            The city object if found, otherwise None.
        """
        if isinstance(city_data, list) and city_data:
            city = city_data[0]
            self.logger.debug(f"Location data is a list, using the first city: {city.name}")
            return city
        elif isinstance(city_data, City):
            self.logger.debug(f"Location data is already a City object: {city_data.name}")
            return city_data
        else:
            self.logger.error(f"Invalid city data provided: {city_data}")
            return None


    def fetch_weather_data_for_city(self, city, start_date, end_date):
        """
        Fetch weather data for a given city from the weather API.

        Parameters
        ----------
        city : City
            The city for which to fetch weather data.
        start_date : str
            The start date for the weather data (yyyy-mm-dd).
        end_date : str
            The end date for the weather data (yyyy-mm-dd).

        Returns
        -------
        WeatherData or None
            The weather data for the city, or None if the data is invalid or fetching failed.
        """
        self.logger.debug(f"Fetching weather data for city: {city.name} (Lat: {city.latitude}, Lon: {city.longitude})")
        
        weather_data = self.weather_service.fetch_weather_data(
            city.latitude, city.longitude, start_date, end_date, city.id
        )

        self.logger.debug(f"location_manager, weather data type {type(weather_data)}")

        return weather_data


    def process_weather_data(self, weather_data, city):
        """
        Processes the fetched weather data, maps it to `DailyWeatherEntry` objects, 
        and stores it in the database.

        Parameters
        ----------
        weather_data : WeatherData
            The fetched weather data to process.
        city : City
            The city associated with the weather data.

        Returns
        -------
        dict
            The processed weather data.
        """
        self.logger.debug(f"Processing weather data for city {city.name}. len {len(weather_data)}")

        try:
            # Map raw weather data to DailyWeatherEntry objects
            for data in weather_data:
                self.db_session.add(data)

            # Commit the transaction
            self.db_session.commit()
            self.logger.debug(f"Weather data successfully added to the database for city {city.name}.")
        except ValueError as e:
            self.logger.error(f"Error processing weather data for {city.name}: {str(e)}")
            return {}

        return weather_data
