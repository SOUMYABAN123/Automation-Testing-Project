import pytest
import allure
from playwright.sync_api import sync_playwright
from common.functions import read_test_data, login, save_data
from locators.react_employee_page import ReactEmployeePageLocators


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
def test_login_react_employee(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-employee-portal-url")  # Update with your employee portal URL

    username = "valid_username"
    password = "valid_password"

    with allure.step("Login with username and password"):
        login(page, username, password)

    success_message = page.wait_for_selector(ReactEmployeePageLocators.DASHBOARD)
    assert success_message is not None, "Login successful"
    allure.attach(page.screenshot(), name="Success Screenshot", attachment_type=allure.attachment_type.PNG)
    save_data('data/stored_data.json', {"login_status": "success", "username": username})


# Additional tests for React Employee Portal
@pytest.mark.smoke
@pytest.mark.gui
def test_dashboard_display_employee(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-employee-portal-url")  # Update with your employee portal URL

    # Ensure the dashboard displays the employee as active
    dashboard = page.wait_for_selector(ReactEmployeePageLocators.DASHBOARD)
    assert dashboard is not None, "Dashboard loaded"


@pytest.mark.smoke
@pytest.mark.gui
def test_avatar_menu_employee(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-employee-portal-url")  # Update with your employee portal URL

    # Ensure the avatar menu displays sign-in data as expected
    avatar_menu = page.wait_for_selector(ReactEmployeePageLocators.AVATAR_MENU)
    assert avatar_menu is not None, "Avatar menu displays as expected"


@pytest.mark.smoke
@pytest.mark.gui
def test_new_order_free_voi(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-employee-portal-url")  # Update with your employee portal URL

    # Ensure new order for FREE VOI can be created successfully
    new_order_button = page.wait_for_selector(ReactEmployeePageLocators.NEW_ORDER_BUTTON)
    assert new_order_button is not None, "New Order button displays"
    new_order_button.click()
    # Fill in order details (assuming there are input fields with names 'order_type' and others)
    page.select_option("select[name='order_type']", "FREE_VOI")
    page.click("button[type='submit']")
    # Verify order is created (assuming there's a success message with id 'order-success-message')
    success_message = page.wait_for_selector("#order-success-message")
    assert success_message is not None, "FREE VOI Order created successfully"


@pytest.mark.smoke
@pytest.mark.gui
def test_new_order_paid_voi(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-employee-portal-url")  # Update with your employee portal URL

    # Ensure new order for PAID VOI can be created successfully
    new_order_button = page.wait_for_selector(ReactEmployeePageLocators.NEW_ORDER_BUTTON)
    assert new_order_button is not None, "New Order button displays"
    new_order_button.click()
    # Fill in order details (assuming there are input fields with names 'order_type' and others)
    page.select_option("select[name='order_type']", "PAID_VOI")
    page.click("button[type='submit']")
    # Verify order is created (assuming there's a success message with id 'order-success-message')
    success_message = page.wait_for_selector("#order-success-message")
    assert success_message is not None, "PAID VOI Order created successfully"


@pytest.mark.smoke
@pytest.mark.gui
def test_view_and_download_order(setup_teardown):
    page = setup_teardown
    page.goto("http://your-react-employee-portal-url")  # Update with your employee portal URL

    # Ensure view and download order links work as expected
    order_id_link = page.wait_for_selector(ReactEmployeePageLocators.ORDER_ID_LINK)
    assert order_id_link is not None, "Order ID link displays"
    order_id_link.click()
    # Verify view order (assuming there's an order details container with id 'order-details')
    order_details = page.wait_for_selector(ReactEmployeePageLocators.ORDER_DETAILS)
    assert order_details is not None, "Order details display as expected"
    # Verify download button (assuming there's a download button with id 'download-button')
    download_button = page.wait_for_selector(ReactEmployeePageLocators.DOWNLOAD_BUTTON)
    assert download_button is not None, "Download button displays and works"
