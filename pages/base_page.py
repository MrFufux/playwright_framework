'''
Parent class containing generic Playwright actions
click, wait, fill, etc
Handles the low-level DOM interactions
OOP Principles: Inheritance, Abstraction, Encapsulation, Polymorphism
SOLID Principles: 

'''
from playwright.sync_api import Page, Locator # Page: single tab or window in the browser, Locator: find elements on a page
from typing import Union #Union: Type Hinting

class BasePage: # class declared
    '''
    The parent class for all Page Objects. 
    It encapsulates standard Playwright interactions to provide an unified, 
    safe, and loggable way to interact with the DOM.
    '''

    # The constructor
    # Automatically runs whenever a new page object is created.
    def __init__(self, page: Page):
        # We take Page object into the constructor
        # and save it as an instance variable(self.page)
        # Every method inside this class now has control of the browser tab
        self.page = page 


    # Custom Navigation method
    #  path = '': the path is optional, if not path -> empty string
    def navigate(self, path: str = ''):
        """Navigates to a specific path using the base_url defined in conftest.py."""
        self.page.goto(path)
        '''
        We configured a base_url in conftest.py file. So Playwright combines the base_url
        and path. If we call a page without the path it will go to the base url.
        '''

    # Click Method reusable(Smart Locators)
    # Accepts a raw locator(CSS, XPath) or a pre-built playwright locator, timeout to 5s
    def click_element(self, locator: Union[str, Locator], timeout: int = 5000):
        """
        Safely clicks an element. Accepts either a CSS/XPath string or a Playwright Locator.
        """
        # ternary operator(Pythonic one-liner): one line if-else. 
        # FLEXIBILITY!! Polymorphism => Method Overloading
        # isinstance: it's a type checking
        element = self.page.locator(locator) if isinstance(locator, str) else locator
        # The condition: if isinstance(locator, str). Is the data passed into the locator variable as str
        # If True: self.page.locator(locator). If it's a string, converts the locator 
        # into a playwright locator using self.page.locator(locator)
        # If False(else):it's already a playwright locator and leave it be.

        element.wait_for(state='visible') # waits the locator to be visible within the DOM
        element.click(timeout=timeout) # performs the click action, applying the explicit timeout

    # Fill Method
    # uses Union for type hinting and requires a str as text and have an explicit wait 
    def fill_text(self, locator: Union[str, Locator], text: str, timeout: int = 5000):
        # ternary operator
        element = self.page.locator(locator) if isinstance(Locator, str) else locator
        # The condition: if isinstance(Locator, str)
        # if True: self.page.locator(locator). If it's a str, converts the locator
        # in to a plawright locator using self.page.locator(locator)
        # If False(else): it's a playwrignt locator and leave it be.

        element.fill(text,timeout=timeout)
        # .fill() waits automatically for the element to be visible, enabled and editable.

    # Wait method
    # waits for a specific UI state
    def wait_for_element_visible(self,locator: Union[str, Locator], timeout: int = 10000):
        # ternary operator
        element = self.page.locator(locator) if isinstance(Locator, str) else locator

        # wait_for() dynamically polls he DOM until the element reaches the desired state
        element. wait_for(state='visible',timeout=timeout)


    
    