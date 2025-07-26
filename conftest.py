import os
import pytest
from dotenv import load_dotenv


def set_test():
    original_value = os.environ.get("CDISC_API_KEY")
    os.environ["CDISC_API_KEY"] = "api_key"
    load_dotenv(".test_env")
    return original_value


def clear_test(original_value):
    if original_value:
        os.environ["CDISC_API_KEY"] = original_value
    load_dotenv(".development_env")


@pytest.fixture(scope="session", autouse=True)
def tests_setup_and_teardown():
    original_value = set_test()
    yield
    clear_test(original_value)
