import pytest
from playwright.sync_api import Page, expect
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_login(page:Page, live_server):
    # ---------------------------------------------------------
    # 1. ARRANGE (Data preparation using Django's ORM)
    # ---------------------------------------------------------
    # Create an user directly in the test db
    test_username = 'candidate_qa'
    test_password = 'Success_interview!W!'
    
    # ORM applied!!
    # SQL Dialect:
    # INSERT INTO auth_user (username, password) 
    # VALUES ('automation_ninja', 'secure_pwd');
    # Replaced by the ORM using plain python code instead SQL dialect
    User.objects.create_user(username=test_username,password=test_password)
    
    # ---------------------------------------------------------
    # 2. ACT Integration with the UI using playwright
    # ---------------------------------------------------------
    # live_server.url. Starts the Django app on a random port (localhost:xxxxx random)
    login_url = f"{live_server.url}/login/"
    page.goto(login_url)
    
    # Filling the form
    page.get_by_text('Username').fill(timeout=2000)
    page.get_by_text('Password').fill(timeout=2000)
    
    page.get_by_role('button', 'submit').click()
               
    # ---------------------------------------------------------
    # 3. ASSERT Validations
    # ---------------------------------------------------------
    # Verifies that the url changesd the dashboard
    expect.to_have_url(f'{live_server.url}/dashboard/')
    
    # Verifies that the welcome message appears
    welcome_message = page.get_by_title('Welcome to the mad house!')
    expect(welcome_message).to_be_enabled()
    expect(welcome_message).to_contain_text(f'Welcome. {test_username}')