# tests/test_login.py

import pytest
import allure
from playwright.sync_api import sync_playwright
from common.functions import read_test_data
from locators.login_page import LoginPageLocators

# Fixture for setting up and tearing down the browser and page
@pytest.fixture(scope="function")
def setup_teardown():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run with UI for debugging
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

# Read the test data
test_data = read_test_data("data/test_data.csv")

# Test function using the setup_teardown fixture and test data
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Login Page Navigation")
@allure.story("Navigate to Login Page and Verify Header")
@pytest.mark.smoke
@pytest.mark.gui
@pytest.mark.debug
@pytest.mark.parametrize("data", test_data)
def test_login_page_header(setup_teardown, data):
    page = setup_teardown

    # Retrieve URLs from test data
    initial_url = data['initial_url']
    login_page_url = data['login_page_url']
    employee_registration_url = data['employee_registration_url']


    # Navigate to the initial URL
    page.goto(initial_url)

    # Find the login link and click it
    with allure.step("Find and click the login link"):
        login_link = page.wait_for_selector(LoginPageLocators.LOGIN_LINK)
        assert login_link is not None, "Login link found"
        login_link.click()

    # Verify redirection to the login page
    with allure.step("Verify redirection to the login page"):
        page.wait_for_url(login_page_url)
        assert page.url.startswith(login_page_url), f"Redirected to the login page: {page.url}"

    # Verify the login page header is displayed
    with allure.step("Verify the login page header"):
        login_page_header = page.wait_for_selector(LoginPageLocators.LOGIN_PAGE_HEADER)
        assert login_page_header is not None, "Login page header found"
        header_text = login_page_header.inner_text().strip()
        assert header_text == "LOGIN", f"Expected header text 'LOGIN', got '{header_text}'"
        allure.attach(page.screenshot(), name="Login Page Screenshot", attachment_type=allure.attachment_type.PNG)
## Added
    # Verify the presence of required sections
    with allure.step("Verify the presence of required sections"):
        sections = [
            ("Commercial Verifier", LoginPageLocators.COMMERCIAL_VERIFIER_HEADING),
            ("Government Verifier", LoginPageLocators.GOVERNMENT_VERIFIER_HEADING),
            ("Employer", LoginPageLocators.EMPLOYER_HEADING),
            ("Employee", LoginPageLocators.EMPLOYEE_HEADING)
        ]
        for section_name, locator in sections:
            try:
                element = page.wait_for_selector(locator, timeout=5000)
                element_text = element.inner_text().strip()
                assert element_text == section_name, f"Expected section heading '{section_name}', got '{element_text}'"
            except TimeoutError:
                pytest.fail(f"Section '{section_name}' not found")

    # Validate 'Register Now' link for Employee and click
    with allure.step("Validate 'Register Now' link for Employee and click"):
        try:
            register_now_link = page.wait_for_selector(LoginPageLocators.EMPLOYEE_REGISTER_NOW_LINK, timeout=5000)
            register_now_link.click()
        except TimeoutError:
            pytest.fail("'Register Now' link for Employee not found")

    # Verify redirection to Employee Registration page
    ##employee_registration_url = "https://app.vaultverify.com/vvapp/Registration_EP.aspx"
    with allure.step("Verify redirection to Employee Registration page"):
        try:
            page.wait_for_url(employee_registration_url, timeout=5000)
            assert page.url.startswith(
                employee_registration_url), f"Expected URL to start with {employee_registration_url}, but got {page.url}"
        except TimeoutError:
            pytest.fail("Did not navigate to the Employee Registration page")

    # Verify 'Employee Registration' header is present
    with allure.step("Verify 'Employee Registration' header is present"):
        try:
            registration_header = page.wait_for_selector(LoginPageLocators.EMPLOYEE_REGISTRATION_HEADER,
                                                         timeout=5000)
            header_text = registration_header.inner_text().strip()
            print(f"Employee Registration header text: '{header_text}'")
            # Perform case-insensitive comparison
            assert header_text.lower() == "employee registration", f"Expected header text 'Employee Registration', got '{header_text}'"
            allure.attach(page.screenshot(), name="Employee Registration Page Screenshot",
                          attachment_type=allure.attachment_type.PNG)
        except TimeoutError:
            page.screenshot(path="error_employee_registration_header.png")
            pytest.fail("'Employee Registration' header not found")