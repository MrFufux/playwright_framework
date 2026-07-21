'''
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

# decorator that automaticallt generates boilerplate code(__init__ and __repr__)
# for classes that stores data
from dataclasses import dataclass 


# Configure logger for API calls

logging.basicConfig(level=logging.INFO) 
# Configures the root logger to output messages at the INFO level or higher 
# (ignorinmg DEBUG messages by default, unless configured otherwise elsewhere)

logging.getLogger(__name__)
# Creates a specific logger instance for this file(__name__ evaluates 
# to the current module's name)

@dataclass # tells python to automatically create an __init__ method
        # for this class using the variables defined below       
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

