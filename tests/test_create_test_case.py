from asserts.api_asserts import create_text_case
from tools.test_data_provider import get_test_data
import pytest


@pytest.mark.parametrize('test_data', get_test_data(__file__))
def test_create_test_cases(test_data, expected_status_code, created_test_case):
    create_text_case(test_data, expected_status_code, created_test_case)
