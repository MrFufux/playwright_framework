import pytest
import httpx
from django.contrib.auth.models import User

# live_server built-in fixture by pytest-django library
# spin up a real instance if the Django app in a background thread
# while the test are running
@pytest.mark.django_db
def test_get_user_profile_api(live_server):
    # ---------------------------------------------------------
    # 1. ARRANGE: We inject the data directly using the Object Relational Mapping ORM
    #
    # ORM: built-in tool on Django that allows me to interact with a 
    # relational database using python code instead raw SQL queries
    # ---------------------------------------------------------
    
    # ORM APPLIED
    User.objects.create_user(username='api_tester', email='qa@tester.com', password='secret_password')
    
    # ---------------------------------------------------------
    # 2. ACT: Real request with httpx to the running server
    # ---------------------------------------------------------
    api_url = f"{live_server.url}/api/users/api_tester"
    
    # If the API requires auth, httpx handles headers easily:
    # response = httpx.get(api_url, headers={"Authorization":"Bearer ... "})
    response = httpx.get(api_url)
    
    # ---------------------------------------------------------
    # 3. ASSERT: We validate the contract and the data
    # ---------------------------------------------------------
    assert response.status_code == 200
    
    data = response.json()
    assert data['username'] == 'api_tester'
    assert data['email'] == 'qa@test.com'
    
    '''
    I chose htppx to ensure the test checks the entire network layer
    
    httpx simulates an exact behavior of an external consumer
    
    keeps the testing framework apart from the development source code
    
    applies some abstraction
    '''