'''
API Tests for GitHub User endpoints.
Demonstrates positive and negative test cases with data-driven approach.
Uses AAA[Arrange, Act, Assert] test pattern
'''

import pytest
from httpx import HTTPStatusError
from fixtures.api_fixture import github_api_client, api_test_data
 
# ------------------------------------------------------------------
# POSITIVE TEST CASES HAPPY PATH
#   GET TESTS
# ------------------------------------------------------------------

@pytest.mark.api_test
def test_get_valid_user_profile(github_api_client):
    # Test: Fetch a valid user's profile
    # Expected: 200 OK with user data
    
    # Arrange. Set up necessary preconditions and inputs.
    username = "octocat" #github demo account
    
    # Act. Executes the single action
    response = github_api_client.get_method(f'/{username}')

    # Assert. Verifies the outcome 
    
    # Uses the helper property built in APIResponse in api_client utils
    assert response.is_success, f'Expected success, got {response.status_code}'
    
    # Verifies the structure of the returned JSON data 
    # (parsed into a Python dict by the client)
    assert response.body['login'] == username
    
    # Verifies if id is in the response body
    assert 'id' in response.body
    
    # Verifies if public_repos is in the response body
    assert 'public_repos' in response.body
    
@pytest.mark.api_test
def test_get_user_repos(github_api_client):
    # Fetch a user's public repositories
    # Expected 200 OK with list of repos
    
    # Arrange
    username = "octocat"
    
    # Act
    response = github_api_client.get_method(f'/{username}')
    
    # Assert
    assert response.is_success
    
    # Verifies that the JSON response was succesfully parsed into a Python list
    assert isinstance(response.body, list) # Expected a list of repositories
    
    # List isn't empty
    assert len(response.body) > 0 # Expected at least one repository
    
    
# ------------------------------------------------------------------
# NEGATIVE TEST CASES SAD PATH XD
# ------------------------------------------------------------------

@pytest.mark.api_test
def test_get_nonexistent_user(github_api_client):
    # Test: Fetch a user that doesn't exist
    # Expected: Raises HTTP error 404 status
    
    # Arrange
    nonexistent_user = "noUSERatALL"
    
    # Act and Assert
   
    with pytest.raises(HTTPStatusError) as exc_info:
        github_api_client.get_method(f'/{nonexistent_user}')
     # This is a context manager
        # APIClient.get() method calls response.raise_for_status()
        # 404 response will crash the Python script
        # This block tells pytest: 'I expect the next line of code to throw
        # this specific error. Catch it, save the error data into exc_info.
        # and pass the test. If it DOES NOT throw an error, fail the test'
        
    # Digs into the caught exception to verify the reason it crashed.
    # Ensures that the response is a 404 http status code
    assert exc_info.value.response.status_code == 404
    
    
# ------------------------------------------------------------------
# DATA-DRIVEN TESTS
# ------------------------------------------------------------------

@pytest.mark.data_test
def test_get_user_with_external_data(github_api_client, api_test_data):
    # Test:Fetch user using data from JSON file
    # This demonstrates the data-drive pattern
    # Change the JSON, and the test automatically uses new data
    
    # Arrange
    # api_test_data[...]: navigates the dict created by JSON fixture
    test_user = api_test_data['github_api']['valid_user']
    username = test_user['username']
    min_repos = test_user['expected_repos_count_min']
    
    # Act
    response = github_api_client.get_method(f'/{username}')
    
    # Assert
    assert response.is_success
    assert response.body['login'] == username
    
    
    
    

    