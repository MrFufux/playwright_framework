'''
API-specific pytest fixtures.
These provide reusable, pre-configured API clients for different endpoints.

Think of fixtures as "setup routines" that inject dependencies into tests.
Tests request them by name in their function signature.
'''
import os #Python's OS interface. Reads environments variables | constructs file paths
import pytest
import httpx
import json
from utils.api_client import APIClient

@pytest.fixture(scope='session')
def github_api_client():
    # Creates a configured API client for GitHub API.
    # Scope='session': Creates ONE client shared across ALL tests in the run.
    # This reuses TCP connections (connection pooling) for better performance.
    
    # os.getenv: checks the system for an environment variable called
    # API_BASE_URL
    # Allows me to easily point my test at a staging env or mocke server in CI/CD
    # without code changes
    base_url = os.getenv("API_BASE_URL", "https://api.github.com")
    
    client = APIClient( # Initiates the custom wrapper
        base_url=base_url,
        timeout=10.0,
        # injects Github-specific headers
        headers={
            "Accept": "vnd.github.v3+json" 
        }
    )
    # yield: this fixture becomes a Generator
    # pauses the function here and gives the client variable 
    # to the test suite.
    yield client
    
    # Teardown: close connections after all tests finish
    client.close()
    
@pytest.fixture(scope='session')
def api_test_data():
    # Loads test data from JSON file
    # Example of data-driven fixture
    # scope = 'session': loads the file once, not per test
    
    # os.path.join: Constructs a file path regardless the OS
    # it navigates up one directory(..), into data_driven_datasets,
    # and targets api_payloads,json
    dataset_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'data_driven_datasets',
        'api_payloads.json'
    )
    # Opens the target JSON file in read mode
    # with: statement that ensures the files is safely closed after reading it
    with open(dataset_path, 'read') as file:
        # Parses the entuire JSON file into Python dict or list
        # and hand it to the tests
        return json.load(file)