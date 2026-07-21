'''
Custom wrapper around HTTPX to handle API authentication headers automatically


Custom wrapper around HTTPX to handle API requests, 
authentication headers, and response validation automatically.

Benefits over raw HTTPX:
- Centralized error handling
- Automatic retries on transient failures
- Response logging for debugging
- Type-safe request methods
'''

import httpx
import logging # python's built-in logging module to track events when run

# type hints, helps to catch error before the code runs
from typing import Optional, Dict, Any

# decorator that automatically generates boilerplate code(__init__ and __repr__)
# for classes that stores data
from dataclasses import dataclass 


# CONFIGURE LOGGER FOR API CALLS

logging.basicConfig(level=logging.INFO) 
# Configures the root logger to output messages at the INFO level or higher 
# (ignorinmg DEBUG messages by default, unless configured otherwise elsewhere)

logger = logging.getLogger(__name__)
# Creates a specific logger instance for this file(__name__ evaluates 
# to the current module's name)

# @dataclass: tells python to automatically create an __init__ method
# for this class using the variables defined below 
@dataclass                 
class APIResponse:
    """Structured response custom object with useful properties. Standardize response"""
    status_code: int # stores HTTP status code
    body: Any # stores parsed JSON data returned by the API
    headers: httpx.Headers # stores HTTP response headers(metadata:content type)

    # @property: Allows access to this method like a regular attribute. 
    # response.is_success instead of response.is_success()]
    @property 
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

# MAIN WRAPPER CLASS
class APIClient:
    """
    Wrapper around HTTPX Client with automatic auth, logging, and error handling.

    Think of this as the "playground" where we make actual API calls
    but with safety nets (retries, timeouts, validation).
    """

    # constructor
    # accepts a base_url, timeout, and custom headers using Optional
    def __init__(self, base_url: str, timeout: float = 10.0,
                 headers: Optional[Dict[str, str]] = None):

    
        # Saves the base URL while stripping trailing extra slashes(/)
        # prevents double-slash error deleting the / from the right 
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout #saves timeout value

        # Default headers (can be overridden)
        # Defines standard header. Indicates the client expects and sends JSON data
        default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # if the user passed in custom headers during initialization,
        # they're merged into default_headers, overriding if there are duplicates
        if headers:
            default_headers.update(headers)

        # Create the a persistent HTTPX session with connection pooling
        # Performance friendly
        # Keeps the underlying TCP connections open(connection pooling)
        self.client = httpx.Client(
            base_url = self.base_url,
            timeout = self.timeout,
            headers = default_headers,
            follow_redirects = True
        )

    # INTERNAL LOGGING HELPERS

    # Private helper method to standardize how outgoing request are logged
    def _log_request(self, method:str, url:str, **kwargs):
        """Log outgoing requests for debugging"""

        # Logs the HTTP method and URL
        logger.info(f"{method.upper()} -> {url}") 
        if 'json' in kwargs: # checks if JSON payload was passed into the request
                
            # Logs the actual data payload
            logger.debug(f"PAYLOAD: {kwargs['json']}")

    # A private helper to standardize how incoming responses are logged
    def _log_response(self, response:httpx.Response):
        """Log responses for debugging"""

        # Logs the status code and the URL that responded
        logger.info(f"RESPONSE: [{response.status_code}] from {response.url}")
            
        # Logs the truncated snippet(first 200 char) of the
        # response body for debugging purposes
        logger.debug(f"RESPONSE body: {response.text[:200]}...")


    # HTTP METHODS (GET, POST, PUT, DELETE)
    # GET method
    def get_method(self, path: str, params:Optional[Dict] = None) -> APIResponse:
        """Perform a GET request"""
        url = f"{self.base_url}/{path.lstrip('/')}" # construct the url with the base_url and lstrip /
        self._log_request('GET', url) # calls the internal logger

        # Executes the HTTP GET request using the persistent session httpx.Client
        response = self.client.get(url, params=params)
        self._log_response(response) # Logs the result

        #Raise exception for 4xx / 5xx 
        # Fail fast mechanism.
        # If the API returns an error code (4xx or 5xx)
        # this line throws a Python exception and stope the code
        # from processing a failed response as if it were success
        response.raise_for_status() 

        # Packages the raw httpx.Response into a clear structured APIResponse data class
        return APIResponse(
            status_code = response.status_code,
            body = response.json(),
            headers=response.headers
        )
        
    # POST method
    def post_method(self, path:str, json_data:Optional[Dict] = None) -> APIResponse:
        #it takes json_data dict
        """Perform a POST request"""
        url = f"{self.base_url}/{path.lstrip('/')}"
        self._log_request("POST", url)
        
        # automatically serializes the python dictionary into a JSON string
        # and sets the correct headers
        response = self.client.post(url, json=json_data)
        self._log_response(response)
        
        response.raise_for_status()
        
        return APIResponse(
            status_code= response.status_code,
            body=response.json(),
            headers=response.headers
        )
        
    # PUT method
    def put_method(self,path:str, json_data:Optional[Dict] = None) -> APIResponse:
        """Perform a PUT request"""
        url = f"{self.base_url}/{path.lstrip('/')}"
        self._log_request("PUT", url)
        
        # automatically serializes the python dictionary into a JSON string
        # and sets the correct headers
        response = self.client.put(url, json=json_data)
        self._log_response(response)
        
        response.raise_for_status()
        
        return APIResponse(
            status_code= response.status_code,
            body=response.json(),
            headers=response.headers  
        )
        
    # DELETE method
    def delete_method(self,path:str) -> APIResponse:
        """Perform a DELETE request"""
        url = f"{self.base_url}/{path.lstrip('/')}"
        self._log_request('DELETE', url)
        
        response = self.client.delete(url)
        self._log_response(response)
        
        response.raise_for_status()
        
        return APIResponse(
            status_code=response.status_code,
            # Safety check
            body=response.json() if response.text else None,
            headers=response.headers
        )
        
    # RESOURCE MANAGEMENT
    def close(self):
        """Close the underlying HTTPX client and release connections"""
        self.client.close()