'''
API Tests for GitHub User endpoints.
Demonstrates positive and negative test cases with data-driven approach.
Uses AAA[Arrange, Act, Assert] test pattern
'''

import pytest
from fixtures.api_fixture import github_api_client, api_test_data
 
# ------------------------------------------------------------------
# POSITIVE TEST CASES HAPPY PATH
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

    
    
    
    

    