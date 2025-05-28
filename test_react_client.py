import pytest
import allure
from playwright.sync_api import sync_playwright
from common.functions import read_test_data, login, save_data
from locators.react_client_page import ReactClientPageLocators


@pytest.fixture(scope="function")
def setup_teardown():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.mark.smoke
@pytest.mark.gui
def test_login_react_client(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-client-portal-url")  # Update with your client portal URL

    username = "valid_username"
    password = "valid_password"

    with allure.step("Login with username and password"):
        login(page, username, password)

    success_message = page.wait_for_selector(ReactClientPageLocators.DASHBOARD)
    assert success_message is not None, "Login successful"
    allure.attach(page.screenshot(), name="Success Screenshot", attachment_type=allure.attachment_type.PNG)
    save_data('data/stored_data.json', {"login_status": "success", "username": username})


@pytest.mark.smoke
@pytest.mark.gui
def test_dashboard_defaults(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-client-portal-url")  # Update with your client portal URL

    dashboard = page.wait_for_selector(ReactClientPageLocators.DASHBOARD)
    assert dashboard is not None, "Dashboard loaded"


@pytest.mark.smoke
@pytest.mark.gui
def test_dashboard_charts(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-client-portal-url")  # Update with your client portal URL

    orders_by_category_chart = page.wait_for_selector("#orders-by-category-chart")
    assert orders_by_category_chart is not None, "Orders by Category chart displays as expected"
    # You can add more chart verifications here


@pytest.mark.smoke
@pytest.mark.gui
def test_dashboard_search(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-client-portal-url")  # Update with your client portal URL

    search_bar = page.wait_for_selector(ReactClientPageLocators.SEARCH)
    assert search_bar is not None, "Search bar displays"
    search_bar.fill("search_term")
    search_bar.press("Enter")

    search_results = page.wait_for_selector("#search-results")
    assert search_results is not None, "Search results display as expected"
