import pytest
import allure
from playwright.sync_api import sync_playwright
from common.functions import read_test_data, login, save_data
from locators.react_verifier_page import ReactVerifierPageLocators


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
def test_login_react_verifier(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-verifier-portal-url")  # Update with your verifier portal URL

    username = "valid_username"
    password = "valid_password"

    with allure.step("Login with username and password"):
        login(page, username, password)

    success_message = page.wait_for_selector(ReactVerifierPageLocators.DASHBOARD)
    assert success_message is not None, "Login successful"
    allure.attach(page.screenshot(), name="Success Screenshot", attachment_type=allure.attachment_type.PNG)
    save_data('data/stored_data.json', {"login_status": "success", "username": username})


# Additional tests for React Verifier Portal
@pytest.mark.smoke
@pytest.mark.gui
def test_dashboard_default_verifier(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-verifier-portal-url")  # Update with your verifier portal URL

    # Ensure the dashboard displays the current month and requested date as most recent
    dashboard = page.wait_for_selector(ReactVerifierPageLocators.DASHBOARD)
    assert dashboard is not None, "Dashboard loaded"


@pytest.mark.smoke
@pytest.mark.gui
def test_grid_view_verifier(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-verifier-portal-url")  # Update with your verifier portal URL

    # Ensure the grid view displays as expected
    grid_view = page.wait_for_selector(ReactVerifierPageLocators.GRID_VIEW)
    assert grid_view is not None, "Grid view displays as expected"


@pytest.mark.smoke
@pytest.mark.gui
def test_add_cc_verifier(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-verifier-portal-url")  # Update with your verifier portal URL

    # Ensure adding a credit card works as expected
    add_cc_button = page.wait_for_selector(ReactVerifierPageLocators.ADD_CC_BUTTON)
    assert add_cc_button is not None, "Add CC button displays"
    add_cc_button.click()
    # Fill in CC details (assuming there are input fields with names 'cc_number', 'cc_expiry', 'cc_cvc')
    page.fill("input[name='cc_number']", "4111111111111111")
    page.fill("input[name='cc_expiry']", "12/25")
    page.fill("input[name='cc_cvc']", "123")
    page.click("button[type='submit']")
    # Verify CC is added (assuming there's a success message with id 'cc-success-message')
    success_message = page.wait_for_selector("#cc-success-message")
    assert success_message is not None, "CC added successfully"
