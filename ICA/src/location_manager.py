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
        """
        self.session_manager.log_session_details()
        self.logger.debug(f"Starting transaction for '{location_name}'")

        # Check if the city already exists in the database
        city = self.get_city_from_db(location_name)
        if city:
            self.logger.info(f"Location '{location_name}' already exists in the database.")
            return [city]

        # Fetch the city data from the API
        location_data_list = self.geocoding_service.fetch_city_data(location_name)
        if len(location_data_list) > 1:
            self.logger.info(f"Multiple locations found for '{location_name}'. Please select one:")
            for idx, loc in enumerate(location_data_list):
                self.logger.debug(f"{idx + 1}. {loc.name}, {loc.country} (Lat: {loc.latitude}, Lon: {loc.longitude})")

            choice = int(input(f"Enter the number of your chosen location (1-{len(location_data_list)}): ")) - 1
            city_info = location_data_list[choice]
            self.logger.debug(f"City info selected, if : {city_info}")
        else:
            city_info = location_data_list[0]
            self.logger.debug(f"City info selected, else: {city_info}")

        # Check if the country exists in the database, create if not
        country = self.get_country_by_id(city_info.country_id, city_info.timezone)
        self.logger.debug(f"City info selected, : {city}, {country}")

        # Now create the city and associate it with the country
        city = self.create_city_entry(city_info, country.id)

        # Commit the transaction
        self.session_manager.log_session_details()
        self.session_manager.commit_session()
        self.logger.info(f"Adding location: {location_name} to the database.")

        return [city]


    def get_country_by_id(self, country_id, timezone):
        """
        Check if the country exists using country_id, otherwise create a new one.

        Parameters
        ----------
        country_id : int
            The ID of the country.
        timezone : str
            Timezone of the country.

        Returns
        -------
        Country
            The country object from the database.
        """
        if not country_id:
            self.logger.error("Country ID is missing or invalid")
            raise ValueError("Country ID is required")

        self.logger.debug(f"Checking if country with ID '{country_id}' exists in the database.")
        country = self.db_session.query(Country).filter_by(id=country_id).first()
        self.logger.debug(f"location_man, country: '{country}' exists in the database.")

        if not country:
            self.logger.warning(f"Country with ID {country_id} not found, creating new entry.")
            # Since we have the timezone, we can create a new country entry
            country = Country(id=country_id, timezone=timezone)
            self.db_session.add(country)
            self.session_manager.commit_session()
            self.logger.debug(f"Country with ID {country_id} added to the database.")
        else:
            self.logger.debug(f"Found existing country with ID {country_id}.")

        return country


    def create_or_get_country(self, country_name, timezone):
        """
        Check if the country exists, otherwise create a new one.

        Parameters
        ----------
        country_name : str
            Name of the country.
        timezone : str
            Timezone of the country.

        Returns
        -------
        Country
            The country object from the database.
        """
        # Check if the city already exists by latitude and longitude
        self.logger.info("checking for country name")
        existing_city = self.db_session.query(City).filter_by(latitude=city_info.latitude, longitude=city_info.longitude).first()
        if existing_city:
            self.logger.debug(f"City {city_info.name} already exists with latitude {city_info.latitude} and longitude {city_info.longitude}.")
        else:
            self.logger.debug(f"City {city_info.name} does not exist. Proceeding with insert.")

        if not country_name:
            self.logger.error("Country name is missing or invalid")
            raise ValueError("Country name is required")

        self.logger.debug(f"Checking if country '{country_name}' exists in the database.")
        country = self.db_session.query(Country).filter_by(name=country_name).first()

        if not country:
            self.logger.warning(f"Country not found, creating new entry for {country_name}")
            country = Country(name=country_name, timezone=timezone)
            self.db_session.add(country)
            self.session_manager.commit_session()
            self.logger.debug(f"Country {country_name} added to the database.")
        else:
            self.logger.debug(f"Found existing country {country_name} with ID {country.id}")

        return country


    def create_city_entry(self, city_info, country_id):
        """
        Create a new city entry in the database.

        Parameters
        ----------
        city_info : City
            The city data to insert.
        country_id : int
            The ID of the country to associate with the city.

        Returns
        -------
        City
            The created city object.
        """
        self.logger.debug(f"Creating city entry for {city_info.name} with country id {country_id}.")
        city = City(
            name=city_info.name,
            latitude=city_info.latitude,
            longitude=city_info.longitude,
            country_id=country_id,
            timezone=city_info.timezone
        )

        self.db_session.add(city)
        self.session_manager.commit_session()
        self.logger.debug(f"City {city_info.name} added to the database.")
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

        if isinstance(city_data, list) and city_data:
            city = city_data[0]
            self.logger.debug(f"Its an instance of list: {city}")
        else:
            print(f"City '{city_data}' not found.")
            return {}

        # Fetch weather data
        self.logger.debug(f"Fetching weather data")
        weather_data = self.weather_service.fetch_weather_data(
            city.latitude, city.longitude, start_date, end_date, city.id
        )
        self.logger.debug(f"location_manager, weather data: {type(weather_data)}, {weather_data}.")

        if not weather_data.is_valid():
            self.logger.error(f"Invalid weather data for city {city_data.name}.")
            return {}

        try:
            daily_weather_entries = weather_data.map_to_daily_weather(city.id)
            self.logger.debug(f"Mapped {len(daily_weather_entries)} daily weather entries.")

            # Add entries to the database
            for entry in daily_weather_entries:
                self.db_session.add(entry)
            self.db_session.commit()
            self.logger.debug("Weather data successfully added to the database.")
        except ValueError as e:
            self.logger.error(f"Error processing weather data: {str(e)}")

        self.logger.debug(f"location_manager, return weather data: {weather_data}.")
        return weather_data