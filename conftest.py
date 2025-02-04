import os
import pytest


def set_test():
    os.environ["PYTHON_ENVIRONMENT"] = "test"


def clear_test():
    os.environ["PYTHON_ENVIRONMENT"] = "development"


@pytest.fixture(scope="session", autouse=True)
def tests_setup_and_teardown():
    set_test()
    yield
    clear_test()
