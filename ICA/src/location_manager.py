import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
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
        self.logger.debug(f"Ensuring country '{city_info.country}' exists in the database.")
        country = self.ensure_country_exists(location_name)

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
        country = self.db_session.query(Country).filter(Country.name.ilike(country_name)).first()
        if not country:
            self.logger.debug(f"Country '{country_name}' not found, creating new entry.")
            country = Country(name=country_name, timezone="Unavailable")
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
        city = self.db_session.query(City).filter_by(name=city_name).first()

        if not city:
            self.logger.debug(f"City '{city_name}' not found, creating new entry.")
            city = City(name=city_name, latitude=latitude, longitude=longitude, timezone="Unavailable", country_id=country.id)
            self.db_session.add(city)
            self.session_manager.commit_session()
            self.logger.info(f"City '{city_name}' added to the database with ID {city.id}.")
        else:
            self.logger.debug(f"City '{city_name}' already exists in the database.")
        
        # Ensure the city is linked to a valid country
        if not city.country:
            self.logger.debug(f"City '{city_name}' does not have a valid country association, linking to country '{country.name}'.")
            city.country = country
            self.db_session.commit()
        
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


    def fetch_weather_data_for_country(self, country, start_date, end_date):
        """
        Fetch weather data for a given country from the weather API.

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
        self.logger.debug(f"Fetching weather data for country: {country}, type: {type(country)}")
        
        weather_data = self.weather_service.fetch_weather_data_for_country(
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
        self.logger.debug(f"Processing weather data for city {city}. len {len(weather_data)}")

        try:
            # Map weather data to DailyWeatherEntry objects
            for data in weather_data:
                # self.logger.debug(f"Mapping raw data for: {data} ")
                self.db_session.add(data)

            # Commit the transaction
            self.db_session.commit()
            self.logger.debug(f"Weather data successfully added to the database for city {city}.")
        except ValueError as e:
            self.logger.error(f"Error processing weather data for {city}: {str(e)}")
            return {}

        return weather_data


    def fetch_seven_day_precipitation(self, location_name, start_date):
        """
        Retrieves 7-day precipitation data from the database or fetches it from Open-Meteo if not found.

        Parameters
        ----------
        location_name : str
            The name of the city.
        start_date : str
            The start date of the 7-day period.

        Returns
        -------
        list
            A list of 7-day precipitation data or None if there is no data.
        """
        # First, check if the precipitation data exists in the database
        weather_data = []
        city = self.get_city_from_db(location_name)
        self.logger.debug(f"7 day dates, start {start_date}")

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        mid_date = start_date + timedelta(days=6)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = mid_date.strftime("%Y-%m-%d")

        # If the city is not found in the database, attempt to fetch weather data
        if not city:
            self.logger.warning(f"City '{location_name}' not found in the database. Fetching data from Open-Meteo.")

            # Fetch city data from the Geocoding API (this returns a list of cities)
            city_data_list = self.geocoding_service.fetch_city_data(city_name=location_name)
            self.logger.debug(f"7 day precip, city_data_list {city_data_list}")

            if city_data_list:
                self.logger.debug(f"7 day precip, {city_data_list[0]}")
                city_info = city_data_list[0]

                # Ensure the city is now a City object
                country = self.ensure_country_exists(location_name)
                city = self.ensure_city_exists(
                    city_info.name, city_info.latitude, city_info.longitude, country
                )

                self.logger.debug(f"Country information received: {country}, City data received: {city}")

                # Now we pass the correct City object
                weather_data = self.fetch_weather_data_for_city(
                    city, start_date, end_date
                )
                self.logger.info(f"7 day precip, weather_data: {weather_data}")

                # If Open-Meteo data is available, process and store it, then return
                if weather_data:
                    self.process_weather_data(weather_data, location_name)
                    return weather_data
                else:
                    self.logger.error(f"No data available for {location_name} from Open-Meteo.")
                    print(f"No data available for {location_name}. Returning to the menu...")
                    return None  # Return to the menu or handle accordingly

        self.logger.debug(f"City '{location_name}' found in the database.")

        # Check if the 7-day precipitation data already exists in the database
        existing_data = self.db_session.query(DailyWeatherEntry.precipitation).filter(
            DailyWeatherEntry.city_id == city.id,
            DailyWeatherEntry.date.between(start_date, end_date)
        ).all()

        if existing_data:
            # Return the existing data if available
            self.logger.info(f"Returning existing precipitation data for {location_name}.")
            return existing_data

        # Process the data and save it to the database
        if weather_data:
            weather_data_obj = WeatherData(weather_data)

            if weather_data_obj.is_valid():
                daily_entries = weather_data_obj.map_to_daily_weather(city.id)
                self.db_session.add_all(daily_entries)
                self.db_session.commit_session()
                self.logger.info(f"Successfully fetched and saved data for {location_name}.")
                return daily_entries
            else:
                self.logger.error(f"Invalid weather data for {location_name}.")
                return None
        else:
            self.logger.error(f"Failed to fetch weather data for {location_name}.")
            return {}

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
        country = self.db_session.query(Country).filter(Country.name.ilike(country_name)).first()

        if not country:
            self.logger.debug(f"Country '{country_name}' not found in the database.")
            return None

        # Define the start and end dates for the year
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        self.logger.debug(f"Received country: {country.name}, start_date: {start_date}, end_date: {end_date})")

        # Query for monthly precipitation totals per city in the country
        monthly_precip = (
            self.db_session.query(
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

        self.logger.debug(f"by country, monthly_precip: {monthly_precip}")

        # Aggregate the data into a dictionary for monthly precipitation
        monthly_data = {month: round(precip, 2) for month, precip in monthly_precip}
        self.logger.debug(f"by country, monthly_data zipped: {monthly_data}")

        # Query for total precipitation for the year
        total_precip = (
            self.db_session.query(func.sum(DailyWeatherEntry.precipitation))
            .join(City, City.id == DailyWeatherEntry.city_id)
            .join(Country, Country.id == City.country_id)
            .filter(Country.id == country.id)
            .filter(DailyWeatherEntry.date.between(start_date, end_date))
            .scalar()
        )

        self.logger.debug(f"by country, total_precip: {total_precip}")

        total_precip = round(total_precip, 2) if total_precip is not None else 0

        self.logger.debug(f"Total precipitation for {country_name} in {year}: {total_precip} mm")

        # Return both the total annual precipitation and the monthly breakdown
        return {
            'total_precipitation': total_precip,
            'monthly_precipitation': monthly_data
        }


    def average_temp_by_city(self, start_date, end_date, location_name):
        self.logger.debug(f"loc man, average_temp_by_city")

        # Get the city object from the database using the location_name
        city = self.get_city_from_db(location_name)
        if not city:
            self.logger.error(f"City '{city}' not found in the database.")
            city_data = self.geocoding_service.fetch_city_data(location_name)

            if not city_data:
                self.logger.error(f"City '{location_name}' could not be fetched from Open-Meteo API.")
                return {}

            # Once the city data is fetched, ensure it is added to the database
            self.logger.debug(f"Adding city '{location_name}' to the database.")
            city = city_data[0]
            self.session_manager.commit_session()

        # Log the city details and fetch weather data
        self.logger.error(f"City '{city}' found in the database.")
        weather_data = self.fetch_weather_data_for_city(city, start_date, end_date)

        self.logger.debug(f"Weather data: {weather_data}")

        # Calculate and return the average temperature
        if weather_data:
            average_temp = sum(entry.mean_temp for entry in weather_data) / len(weather_data)
            return average_temp
        else:
            self.logger.error(f"No weather data available for city '{city.name}' within the specified range.")
            return {}
