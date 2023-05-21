""" This module contains all necessary tools for test_data """
import logging
import os

import pytest
import yaml


def get_test_data(test_path: str):
    """
    Collect full test data for running.

    1. Extract the directory and test set name from the test_path.
    2. Load the full test data from the YAML file.
    3. Extract the general test data
    4. Extract the test set data
    5. Create a list of the general test data and the test set data
    :param test_path: The path to the YAML file containing the test data.

    return: list with test data.
    """
    directory = os.path.dirname(test_path)
    test_set_name = os.path.splitext(os.path.basename(test_path))[0]

    logging.info(f"Get test name {test_set_name}")

    test_data = os.path.join(directory, "test_data.yml")

    logging.info(f"Get full test data by path: {test_data}")

    with open(test_data, 'r') as file:
        data = yaml.safe_load(file)

    general_data = data.get("general")
    general_data = {"general": general_data}

    tests_set = data.get("test_sets")
    test_data_set = {"test_data_set": tests_set.get(test_set_name)}

    test_parameters = []
    test_parameters.append(pytest.param({**general_data, **test_data_set}))

    return test_parameters
