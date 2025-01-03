import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from base_api_service import BaseApiService
from session_manager import SessionManager
from models import *

class GeocodingApiService(BaseApiService):
    """
    Service for interacting with the Open-Meteo Geocoding API.
    """

    def __init__(self, session_manager: SessionManager, max_retries=3, retry_delay=2):
        super().__init__(base_url="https://geocoding-api.open-meteo.com/v1/search", max_retries=max_retries, retry_delay=retry_delay)
        self.session = session_manager.get_session()


    def fetch_city_data(self, city_name):
        """
        Fetches geocoding data for a given city name from the Open-Meteo API, processes the data,
        and saves the city information (and optional country) to the database.

        Args:
            city_name (str): The name of the city to fetch data for.

        Returns:
            list: A list containing the `City` object(s) added to the database.
        
        Raises:
            ValueError: If no results are found for the given city name.
            SQLAlchemyError: If there is a database-related error during the transaction.
            Exception: If any other unexpected error occurs.
        """
        self.logger.debug(f"Fetching geocoding data for city: {city_name}")
        try:
            # Fetch city data from the API
            response = self._make_request(params={'name': city_name})
            # self.logger.debug(f"API Response: {response}")
            data = response.get("results", [])

            if response and response.get("results"):
                self.logger.info(f"Found {len(response['results'])} results for {city_name}")
            else:
                self.logger.error(f"No results found for {city_name}")            
                raise ValueError(f"No results found for city: {city_name}")

            # Handle multiple city results
            if len(data) > 1:
                print(f"Multiple locations found for '{city_name}':")
                for idx, city in enumerate(data):
                    # Use country or country_code
                    country_display = city.get('country', city.get('country_code', 'N/A'))
                    print(f"{idx + 1}. {city['name']}, {country_display} (Lat: {city['latitude']}, Lon: {city['longitude']})")

                # Get user choice
                try:
                    choice = int(input(f"Please select a city (1-{len(data)}): ")) - 1
                    if choice < 0 or choice >= len(data):
                        raise ValueError("Invalid choice")
                except ValueError as e:
                    self.logger.error(f"Invalid city choice: {e}")
                    print("Please enter a valid number.")
                    return self.fetch_city_data(city_name)
                
                city_info = data[choice]
            else:
                city_info = data[0]

            self.logger.debug(f"City selected: {city_info}")
            self.logger.debug(f"City keys: {city_info.keys()}")

            # Ensure the city data has required fields
            if 'name' not in city_info or 'latitude' not in city_info or 'longitude' not in city_info:
                self.logger.error(f"Incomplete city data: {city_info}")
                raise ValueError(f"Incomplete data for city: {city_info}")

            # Attempt to get the country (check if 'country' is present)
            country_name = city_info.get('country', None) or city_info.get('country_code', None)  # Try country first, then country_code
            country = None
            if country_name:
                self.logger.debug(f"Extracted country: {country_name} from city info")
                self.logger.debug(f"Searching for country: {country_name}")
                
                # Check if the country already exists in the database
                country = self.session.query(Country).filter_by(name=country_name).first()
                
                if country:
                    self.logger.debug(f"Country {country_name} already exists in the database, skipping creation.")
                else:
                    # Country not found, adding it to the database
                    self.logger.debug(f"Country not found in database. Adding new country: {country_name}")
                    country = Country(name=country_name, timezone=city_info.get('timezone', 'Unavailable'))
                    self.session.add(country)
                    self.session.commit()
            else:
                # Log a warning if no country is found in the API data
                self.logger.warning(f"No country found for city: {city_info['name']}. Storing as unavailable.")
                # Save as unavailable if no country data
                country = Country(name="Unavailable", timezone="Unavailable")
                self.session.add(country)
                self.session.commit()

            # Insert city data (even if no country is linked)
            self.logger.debug(f"Creating city with name: {city_info['name']}, Latitude: {city_info['latitude']}, Longitude: {city_info['longitude']}")
            city = City(
                name=city_info['name'],
                latitude=city_info['latitude'],
                longitude=city_info['longitude'],
                timezone=city_info.get('timezone'),
                country_id=country.id if country else None  
            )
            self.session.add(city)
            self.session.commit()
            self.logger.debug(f"City {city.name} added to the database with ID {city.id}")
            return [city]

        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Database error occurred while adding city: {e}")
            raise

        except ValueError as e:
            self.logger.error(f"Value error occurred: {e}")
            raise

        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Unexpected error occurred: {e}")
            raise