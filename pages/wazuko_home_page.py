'''
A child class
Represents a specific view in the app.
Contains: locators and bussiness flows for that specific page

'''
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class WazukoHomePage(BasePage): # this class inherits from BasePage
    """
    Page Object for the main www.wazoku.com homepage.
    Handles all UI locators and interactions for this specific view.
    """

    # constructor
    def __init__(self, page: Page):
        # Passes the page onject up to the parent BasePage class
        # so its methods can function
        super().__init__(page) 


        # Locators (instance variables)
        # Main options: 
        self.who_we_are_button = self.page.get_by_role('button', name='Who we are')
        self.where_we_help_button = self.page.get_by_role('button',name='Where we help')

        # options inside main options
        self.join_us_option = self.page.get_by_text('Join us')
        self.water_option = self.page.get_by_text('Water')

        self.talk_to_an_expert_option = self.page.get_by_role('link', name='Talk to an Expert')

    
    # Actions (Methods)

    def open_what_we_do_menu(self):
        #clicks the Who we are button reusing the click_element BasePage method
        self.click_element(self.who_we_are_button)

    def open_where_we_help_menu(self):
        self.click_element(self.where_we_help_button)

    
