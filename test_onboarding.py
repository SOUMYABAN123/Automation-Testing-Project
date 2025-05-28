import pytest
import allure
from playwright.sync_api import sync_playwright
from common.functions import read_test_data, complete_onboarding, save_data
from locators.onboarding_page import OnboardingPageLocators


@pytest.fixture(scope="function")
def setup_teardown():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.mark.parametrize("data", read_test_data("data/onboarding_data.csv"))
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Onboarding Tests")
@allure.story("User Onboarding Functionality")
@pytest.mark.regression
@pytest.mark.gui
def test_onboarding(setup_teardown, data):
    page = setup_teardown
    page.goto("http://your-vault-system-onboarding-url")  # Update with your onboarding URL

    first_name = data['first_name']
    last_name = data['last_name']
    expected_result = data['expected_result']

    with allure.step("Complete onboarding steps"):
        complete_onboarding(page, first_name, last_name)

    if expected_result == 'success':
        success_message = page.wait_for_selector(OnboardingPageLocators.SUCCESS_MESSAGE)
        assert success_message is not None, "Onboarding successful"
        allure.attach(page.screenshot(), name="Success Screenshot", attachment_type=allure.attachment_type.PNG)
        save_data('data/stored_data.json',
                  {"onboarding_status": "success", "first_name": first_name, "last_name": last_name})
    else:
        error_message = page.wait_for_selector(OnboardingPageLocators.ERROR_MESSAGE)
        assert error_message is not None, "Error message displayed"
        allure.attach(page.screenshot(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        save_data('data/stored_data.json',
                  {"onboarding_status": "failure", "first_name": first_name, "last_name": last_name})
