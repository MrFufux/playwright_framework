import pytest
from pages.wazuko_home_page import WazukoHomePage
from playwright.sync_api import expect, Page

@pytest.mark.ui_test
def test_where_we_help_option(ui_page: Page):

    # Following the AAA Arrange-Act-Assert
    # 1. ARRANGE: Set up the page object
    home_page = WazukoHomePage(ui_page)

    # 2. ACT: Perform the user journey
    home_page.accept_cookies_option()
    home_page.open_where_we_help_menu()
    home_page.open_water_option()

    # 3. ASSERT: Verify the expected outcomes
    expect.soft(home_page.talk_to_an_expert_option).to_be_enabled()
    expect.soft(home_page.talk_to_an_expert_option).to_have_text('Talk to an Expert')
    # to_have_text(): automatically waits for the element to be visible