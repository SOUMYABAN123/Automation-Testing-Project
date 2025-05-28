import pytest
import allure
from playwright.sync_api import sync_playwright
from common.functions import read_test_data, register, save_data
from locators.registration_page import RegistrationPageLocators


@pytest.fixture(scope="function")
def setup_teardown():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.mark.parametrize("data", read_test_data("data/registration_data.csv"))
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Registration Tests")
@allure.story("User Registration Functionality")
@pytest.mark.regression
@pytest.mark.gui
def test_registration(setup_teardown, data):
    page = setup_teardown
    page.goto("http://your-vault-system-registration-url")  # Update with your registration URL

    username = data['username']
    password = data['password']
    confirm_password = data['confirm_password']
    email = data['email']
    expected_result = data['expected_result']

    with allure.step("Register with provided details"):
        register(page, username, password, confirm_password, email)

    if expected_result == 'success':
        success_message = page.wait_for_selector(RegistrationPageLocators.SUCCESS_MESSAGE)
        assert success_message is not None, "Registration successful"
        allure.attach(page.screenshot(), name="Success Screenshot", attachment_type=allure.attachment_type.PNG)
        save_data('data/stored_data.json', {"registration_status": "success", "username": username})
    else:
        error_message = page.wait_for_selector(RegistrationPageLocators.ERROR_MESSAGE)
        assert error_message is not None, "Error message displayed"
        allure.attach(page.screenshot(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        save_data('data/stored_data.json', {"registration_status": "failure", "username": username})


# Additional tests for different types of registrations
@pytest.mark.regression
@pytest.mark.gui
def test_register_commercial_verifier(setup_teardown):
    page = setup_teardown
    page.goto("http://your-vault-system-registration-url/commercial-verifier")  # Update with your URL

    username = "commercial_verifier"
    password = "password"
    confirm_password = "password"
    email = "commercial_verifier@example.com"

    with allure.step("Register Commercial Verifier"):
        register(page, username, password, confirm_password, email)

    success_message = page.wait_for_selector(RegistrationPageLocators.SUCCESS_MESSAGE)
    assert success_message is not None, "Commercial Verifier Registration successful"
    allure.attach(page.screenshot(), name="Success Screenshot", attachment_type=allure.attachment_type.PNG)
    save_data('data/stored_data.json', {"registration_status": "success", "username": username})


@pytest.mark.regression
@pytest.mark.gui
def test_register_government_verifier(setup_teardown):
    page = setup_teardown
    page.goto("http://your-vault-system-registration-url/government-verifier")  # Update with your URL

    username = "government_verifier"
    password = "password"
    confirm_password = "password"
    email = "government_verifier@example.com"

    with allure.step("Register Government Verifier"):
        register(page, username, password, confirm_password, email)

    success_message = page.wait_for_selector(RegistrationPageLocators.SUCCESS_MESSAGE)
    assert success_message is not None, "Government Verifier Registration successful"
    allure.attach(page.screenshot(), name="Success Screenshot", attachment_type=allure.attachment_type.PNG)
    save_data('data/stored_data.json', {"registration_status": "success", "username": username})
