import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddfsdw001 import RuleDDFSDW001
from usdm3.rules.library.rule_template import RuleTemplate
from tests.helpers.rule_error import error_timestamp


@pytest.fixture
def rule():
    return RuleDDFSDW001()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDFSDW001"
    assert rule._level == RuleTemplate.ERROR
    assert rule._rule_text == "The version in the wrapper should be set to 3.0.0"
    assert rule._errors.count() == 0


def test_validate_valid(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "usdmVersion": "3.0.0",
        },
    ]

    config = {"data": data_store}
    assert rule.validate(config) is True
    assert rule._errors.count() == 0


def test_validate_missing_code_system_version(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {"version": "3.0.0"},
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "usdmVersion",
            "klass": "Wrapper",
            "path": "path/path1",
            "rule": "DDFSDW001",
            "rule_text": "The version in the wrapper should be set to 3.0.0",
        },
        "message": "Invalid version detected, not set to 3.0.0",
        "type": "DDFSDW001",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }
