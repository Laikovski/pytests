"""Module contains necessary fixtures."""
import logging
from typing import Union

import pytest
import os

from core.client import APIClient


@pytest.fixture()
def credentials(test_data) -> dict:
    """
    Return the username and password credentials for the test.

    :param test_data: A dictionary containing test data.
    :return: A dictionary containing the credentials.
    """
    if (username := os.getenv("USERNAME")) and (password := os.getenv("PASSWORD")):
        cred = {"username": username,
                "password": password}

    elif general_data := test_data.get("general"):
        cred = {"username": general_data.get("username"),
                "password": general_data.get("password")}

    else:
        cred = None

    return cred


@pytest.fixture()
def expected_status_code(test_data: dict) -> Union[str, None]:
    """
    Return the expected HTTP status code for the test, if specified in the test data.

    :param test_data: A dictionary containing test data.
    :return: The expected HTTP status code, or None if not specified.
    """
    test_data_set = test_data.get("test_data_set")

    if expected_response := test_data_set.get("status_code"):
        logging.info(f"Get expected response code")
        return expected_response
    else:
        return None


@pytest.fixture()
def endpoint(test_data: dict) -> Union[str, None]:
    """
    Return endpoint for tests.

    :param test_data: A dictionary containing test data.
    :return: endpoint, or None if not specified.
    """
    test_data_set = test_data.get("test_data_set")

    if endpoint := test_data_set.get("end_point"):
        logging.info(f"Get particular endpoint")
        return endpoint
    else:
        return None


@pytest.fixture()
def api_client(credentials: dict) -> APIClient:
    """
    Return an instance of the APIClient class, which is used to make HTTP requests to the API being tested.

    :param credentials: A dictionary containing the username and password for the API client.
    :return: An instance of the APIClient class.
    """
    return APIClient(credentials.get("username"), credentials.get("password"))


@pytest.fixture()
def created_test_suit(api_client: APIClient):
    """
    Pytest fixture that creates a test suite using the provided API client, and deletes all test suites after.

    :param api_client: An instance of the APIClient class to use for API requests.
    :return: The response object returned by the API when creating the test suite.
    """
    logging.info(f"Create suit case")

    params = {
        'title': "basic suit test",
    }
    test_suit = api_client.post('/test_suites', json=params)

    yield test_suit

    logging.info(f"Delete all suits")

    api_client.delete('/test_suites')


@pytest.fixture()
def created_test_case(api_client: APIClient, created_test_suit):
    """
    Pytest fixture that creates a test case using the provided API client.

    :param api_client: An instance of the APIClient class to use for API requests.
    :param created_test_suite: A fixture that creates a test suite using the provided API client.
    :return: The response object returned by the API when creating the test case.
    """
    logging.info(f"Create test case")

    params = {
        "suiteID": created_test_suit.json().get('id'),
        "title": "test case name",
        "description": "short info about test case"
    }
    yield api_client.post('/test_cases', json=params)

    logging.info(f"Delete all test cases")

    api_client.delete('/test_cases')
