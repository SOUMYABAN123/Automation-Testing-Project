import pytest
import allure
from common.functions import read_test_data, api_login, save_data

BASE_URL = "http://your-vault-system-api-url"  # Update with your API URL


@pytest.mark.parametrize("data", read_test_data("data/test_data.csv"))
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("API Login Tests")
@allure.story("API Login Functionality")
@pytest.mark.smoke
@pytest.mark.api
def test_api_login(data):
    username = data['username']
    password = data['password']
    expected_result = data['expected_result']

    response = api_login(BASE_URL, username, password)

    if expected_result == 'success':
        assert response.status_code == 200, "Login successful"
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
        save_data('data/stored_data.json', {"api_login_status": "success", "username": username})
    else:
        assert response.status_code != 200, "Login failed"
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
        save_data('data/stored_data.json', {"api_login_status": "failure", "username": username})


# Additional tests for WAPI, payroll, and roster
@pytest.mark.api
def test_wapi_term_ee(api_client):
    response = api_client.get("/wapi/term-ee")
    assert response.status_code == 200, "WAPI Term EE API call successful"
    allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)


@pytest.mark.api
def test_wapi_voe_match(api_client):
    response = api_client.get("/wapi/voe-match")
    assert response.status_code == 200, "WAPI VOE Match API call successful"
    allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)


@pytest.mark.api
def test_wapi_voi_match(api_client):
    response = api_client.get("/wapi/voi-match")
    assert response.status_code == 200, "WAPI VOI Match API call successful"
    allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)


@pytest.mark.api
def test_roster_data(api_client):
    response = api_client.get("/roster-data")
    assert response.status_code == 200, "Roster data API call successful"
    allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)


@pytest.mark.api
def test_payroll_data(api_client):
    response = api_client.get("/payroll-data")
    assert response.status_code == 200, "Payroll data API call successful"
    allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
