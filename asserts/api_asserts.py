"""Asserts for API tests."""

from core.client import APIClient

import logging


def soft_check_status_code(test_data: dict, expected_status_code: str, actual_response: str):
    """Perform a soft check of the status code for the given test data.

    :param test_data: A dictionary containing the test data.
    :param expected_status_code: The expected HTTP status code.
    :param actual_response: The actual HTTP status code returned by the API.
    """
    test_data_set = test_data.get("test_data_set")
    test_name = test_data_set.get("test_name")

    logging.info(f"Soft check 'status code' for test: {test_name}")

    assert expected_status_code == actual_response, \
        f"Expected status code: {expected_status_code}, actual_status_code: {actual_response}"


def check_authentication(test_data: dict, expected_status_code: str, api_client: APIClient):
    """Check the authentication status for the given test data.

    :param test_data: A dictionary containing the test data.
    :param expected_status_code: The expected HTTP status code.
    :param api_client: An instance of APIClient to use for the API request.
    """
    auth_response = api_client.response.status_code

    soft_check_status_code(test_data, expected_status_code, auth_response)

    assert api_client.response.json().get("access_token"), "Key not found"


def check_wrong_authentication(test_data, expected_status_code):
    """
    Check the authentication status with wrong username and password.

    :param test_data: A dictionary containing the test data.
    :param expected_status_code: The expected HTTP status code.
    :param api_client: An instance of APIClient to use for the API request.
    :param test_data:
    :param expected_status_code:
    :param api_client:
    """
    test_data_set = test_data.get('test_data_set')
    username = test_data_set.get("username")
    password = test_data_set.get("password")

    client = APIClient(username, password)

    soft_check_status_code(test_data, expected_status_code, client.response.status_code)

    expected_messages = test_data_set.get('message')
    assert client.response.json().get('message') == expected_messages, f"Message: {expected_messages} not received "


def get_all_text_cases(test_data: dict, expected_status_code: str, endpoint: str, created_test_case,
                       api_client: APIClient):
    """
    Test function that sends a GET request to the specified API endpoint.

    :param test_data: A dictionary containing any additional test data to be used in the test.
    :param expected_status_code: The expected HTTP status code of the API response.
    :param endpoint: The API endpoint to test.
    :param api_client: An instance of the APIClient class to send requests through.
    """
    get_test_cases = api_client.get(endpoint)
    actual_status_code = get_test_cases.status_code
    soft_check_status_code(test_data, expected_status_code, actual_status_code)

    assert len(get_test_cases.json().get('test_cases')) >= 1, "Tests cases not found"


def delete_all_text_cases(test_data: dict, expected_status_code: str,
                          endpoint: str, created_test_case, api_client: APIClient):
    """
    Delete all test cases for the given endpoint using the `delete()` method.

    :param test_data: A dictionary containing any additional test data to be used in the test.
    :param expected_status_code: The expected HTTP status code of the API response.
    :param endpoint: The API endpoint to test.
    :param api_client: An instance of the APIClient class to send requests through.
    """
    get_test_cases = api_client.get(endpoint)
    actual_status_code = get_test_cases.status_code
    soft_check_status_code(test_data, expected_status_code, actual_status_code)

    api_client.delete(endpoint)
    get_test_cases = api_client.get(endpoint)

    assert get_test_cases.json().get("test_cases") == [], "Tests cases not deleted"


def create_text_case(test_data: dict, expected_status_code: str, created_test_case):
    """
    Assert created test case.
    :param test_data: A dictionary containing any additional test data to be used in the test.
    :param expected_status_code: The expected HTTP status code of the API response.
    :param created_test_case: creates a test case using the provided API client
    """
    actual_status_code = created_test_case.status_code
    soft_check_status_code(test_data, expected_status_code, actual_status_code)

    response_message = test_data.get("test_data_set").get("message")

    assert created_test_case.json().get("message") == response_message, "Tests cases not created"
