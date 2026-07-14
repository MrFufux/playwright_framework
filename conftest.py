'''
"Heart of pytest"
Dependency injection hub.
Holds all the fixtures (setup and teardown functions)
The tests files stay clean

'''

import pytest
import httpx
from typing import Generator
from playwright.sync_api import Page

# ----------------------------------------------------------------------
# 1. PLAYWRIGHT BROWSER CONTEXT CONFIGURATION
# ----------------------------------------------------------------------
@pytest.fixture(scope='session')
def browser_context_args(browser_context_args: dict) -> dict:
    """
    Intercepts and overrides the default Playwright browser context.
    Demonstrates environment control for CI/CD consistency.
    """
    return {
        # **: takes all the existing key-value pairs from the default browser_context_args dict 
        # and put it (merges) into a new dict that I'm creating.
        # Add custom settings without losing the original data.
        **browser_context_args,     
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        # Base URL allows tests to just say page.goto("/login") 
        # instead of the full domain, making it easy to swap between staging/prod.
        "base_url": "www.page.com"
        '''
        I overrride the browser_context_args fixture to force strict viewports
        Ensures our CI Pipeline on jenkins runs in the same state as my local machine
        This eliminates flakiness

        If the devs change the version of the api, I only need to update the URL in one single file
        (conftest.py) and not hunting down hundreds of strings accross the test scripts.
        '''
    }

# ----------------------------------------------------------------------
# 2. CUSTOM UI PAGE WRAPPER
# ----------------------------------------------------------------------
@pytest.fixture(scope='function')
def ui_page(page:Page) -> Generator[Page, None, None]:
    """
    Custom fixture that wraps the default Playwright page.
    It automatically navigates to the base URL before the test starts,
    keeping our test files DRY (Don't Repeat Yourself).
    """
    # Setup: Go to the homepage before the test begins
    page.goto('/')

    # Yield hands control over to the actual test function
    yield page
    '''
    I use yield in pytest fixtures, because it allows me to cleanly encapsulate
    the setup and teardown logic in a single function.

    With return, the function would terminate and I would have no way to execute cleanup code
    (clearing cookies or closing connections) after the test finishes.

    Yield pauses the fixture, allows the test to run and then the clean up happens and do not leave
    any garbage when the test is over.
    '''

    # Teardown (Optional): We could clear local storage or cookies here if needed,
    # though Playwright's isolated contexts usually handle this for us automatically.

# ----------------------------------------------------------------------
# 3. HTTPX API CLIENT (PERFORMANCE OPTIMIZED)
# ----------------------------------------------------------------------
# scoper per sessions maintains the TCP 3-way hadshake and TLS/SSL negotiation to establish connection.
@pytest.fixture(scope='session')
def api_client() -> Generator[httpx.Client, None, None]:
    # httpx.Client() opens a single connection pool. It keeps the TCP/TLS connection alive.
    # Setup
    with httpx.Client(
        base_url="https://api.github.com",
        timeout=10.0, # hardcoded timeout: fail fast and prevents CI/CD pipeline freezes
        headers={"Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
            }
    ) as client: # Teardown. When the test finishes, it closes all the connections
        yield client