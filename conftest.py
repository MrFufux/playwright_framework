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
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        # Base URL allows tests to just say page.goto("/login") 
        # instead of the full domain, making it easy to swap between staging/prod.
        "base_url": 'www.page.com'
    }
