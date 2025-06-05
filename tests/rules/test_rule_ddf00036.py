import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00036 import RuleDDF00036
from usdm3.rules.library.rule_template import RuleTemplate
from tests.helpers.rule_error import error_timestamp


@pytest.fixture
def rule():
    return RuleDDF00036()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00036"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == 'If timing type is "Fixed Reference" then the corresponding attribute relativeToFrom must be filled with "Start to Start".'
    )
    assert rule._errors.count() == 0


def test_validate_valid(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Fixed Reference"},
            "instanceType": "Timing",
            "relativeToFrom": {"decode": "Start to Start"},
        }
    ]

    config = {"data": data_store}

    assert rule.validate(config) is True
    assert rule._errors.count() == 0


def test_validate_invalid_both_references(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Fixed Reference"},
            "instanceType": "Timing",
            "relativeToFrom": {"decode": "Not Start to Start"},
        }
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}

    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "relativeToFrom",
            "klass": "Timing",
            "path": "path/path1",
            "rule": "DDF00036",
            "rule_text": 'If timing type is "Fixed Reference" then the corresponding attribute relativeToFrom must be filled with "Start to Start".',
        },
        "message": "Invalid relativeToFrom",
        "type": "DDF00036",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }
