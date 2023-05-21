"""Module consists connection client with necessary methods."""
from core.const import Constants
import requests


class APIClient:
    """A client for making HTTP requests to the API."""

    def __init__(self, username, password):
        """
        Initialize the APIClient instance.

        :param username: The username to use for authentication.
        :param password: The password to use for authentication.
        """
        self.base_url = Constants.BASIC_URL
        self.session = requests.Session()

        self.token = None

        self.response = self.authenticate(username, password)

    def authenticate(self, username: str, password: str):
        """
        Authenticate user and get token.

        :param username: The username to use for authentication.
        :param password: The password to use for authentication.
        :return: response
        """
        auth_url = f"{self.base_url}/login"
        response = self.session.post(auth_url, json={"username": username, "password": password})

        if response.status_code == 200:
            self.token = response.json().get("access_token")

        self.token = response.json().get("access_token")

        return response

    def get(self, path, **kwargs):
        """
        Send a GET request to the API.

        :param path: The path of the endpoint to call.
        :param **kwargs: Additional arguments to pass to the `requests.get()` method.
        :return: The response object returned by the API.
        """
        headers = self._get_headers()
        url = f"{self.base_url}{path}"
        return self.session.get(url, headers=headers, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        """
        Send a POST request to the API.

        :param path: The path of the endpoint to call.
        :param data: The data to send in the request body.
        :param json: The JSON data to send in the request body.
        :param **kwargs: Additional arguments to pass to the `requests.post()` method.
        :return: The response object returned by the API.
        """
        headers = self._get_headers()
        url = f"{self.base_url}{path}"
        return self.session.post(url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, path, **kwargs):
        """
        Send a DELETE request to the API.

        :param path: The path of the endpoint to call.
        :param **kwargs: Additional arguments to pass to the `requests.delete()` method.
        :return: The response object returned by the API.
        """
        headers = self._get_headers()
        url = f"{self.base_url}{path}"
        return self.session.delete(url, headers=headers, **kwargs)

    def _get_headers(self):
        """
        Get the headers to use for API requests.

        :return: A dictionary containing the headers to use for API requests.
        """
        headers = {"Content-Type": "application/json"}

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers
