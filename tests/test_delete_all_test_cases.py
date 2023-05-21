from asserts.api_asserts import delete_all_text_cases
from tools.test_data_provider import get_test_data
import pytest


@pytest.mark.parametrize('test_data', get_test_data(__file__))
def test_get_all_test_cases(test_data, expected_status_code, endpoint, created_test_case, api_client):
    delete_all_text_cases(test_data, expected_status_code, endpoint, created_test_case, api_client)
