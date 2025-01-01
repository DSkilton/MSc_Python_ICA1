import requests
import time
import logging 

class BaseApiService:
    """
    Base class for shared API service logic.
    Provides retry functionality, request execution, and error handling.
    """

    def __init__(self, base_url, max_retries=3, retry_delay=2):
        """
        Initialize the BaseApiService.

        Parameters
        ----------
        base_url : str
            The base URL for the API.
        max_retries : int
            Maximum number of retry attempts for failed API calls.
        retry_delay : int
            Delay (in seconds) between retries.
        """
        self.base_url = base_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"BaseApiService initialized with base_url={base_url}, max_retries={max_retries}, retry_delay={retry_delay}")


    def _make_request(self, endpoint="", params=None):
        """
        Execute an HTTP GET request with retry logic.

        Parameters
        ----------
        endpoint : str
            The specific endpoint to append to the base URL.
        params : dict
            Query parameters for the GET request.

        Returns
        -------
        dict
            Parsed JSON response from the API.

        Raises
        ------
        Exception
            If all retry attempts fail or the response is invalid.
        """
        self.logger.debug(f"Attempting to make request to {self.base_url}/{endpoint} with params {params}")

        url = f"{self.base_url}/{endpoint}".strip("/")
        params = params or {}

        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"Attempt {attempt}: Requesting {url} with params {params}")
                response = requests.get(url, params=params)
                response.raise_for_status()
                self.logger.debug(f"Request succeeded on attempt {attempt}, Response: {response}")
                data = response.json()

                if not isinstance(data, dict) not in data:
                    self.logger.error(f"Invalid response structure from API: {type(data)}, {data}")
                    raise ValueError("Invalid response structure from API.")
                self.logger.debug(f"Request succeeded on attempt {attempt}")
                # self.logger.debug(f"Base_api, data to be returned {data}")
                return data
            except requests.RequestException as e:
                self.logger.error(f"Attempt {attempt} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    raise Exception(f"Failed to fetch data from {url} after {self.max_retries} attempts")
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"HTTP error occurred: {e}")
                raise
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error in making request to {url}: {e}")
                raise
