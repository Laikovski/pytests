from asserts.api_asserts import check_wrong_authentication
from tools.test_data_provider import get_test_data
import pytest


@pytest.mark.parametrize('test_data', get_test_data(__file__))
def test_smoke(test_data, expected_status_code):
    check_wrong_authentication(test_data, expected_status_code)
