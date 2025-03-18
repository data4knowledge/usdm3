import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00025 import RuleDDF00025
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00025()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00025"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == 'A window must not be defined for an anchor timing (i.e., type is "Fixed Reference").'
    )
    assert rule._errors.count() == 0


def test_validate_valid_timing(rule):
    """Test validation with valid timeline exit reference"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "t1",
            "instanceType": "Timing",
            "type": {"decode": "Fixed Reference"},
        },
        {
            "id": "t2",
            "instanceType": "Timing",
            "type": {"decode": "Fixed Reference"},
        },
        {
            "id": "t3",
            "instanceType": "Timing",
            "type": {"decode": "Fixed Reference"},
            "windowLoweer": None,
        },
        {
            "id": "t3",
            "instanceType": "Timing",
            "type": {"decode": "Fixed Reference"},
            "windowUpper": None,
        },
        {
            "id": "t3",
            "instanceType": "Timing",
            "type": {"decode": "Fixed Reference"},
            "windowLoweer": None,
            "windowUpper": None,
        },
        {
            "id": "t6",
            "instanceType": "Timing",
            "type": {"decode": "Other"},
            "windowLower": "1",
            "windowUpper": "2",
        },
    ]

    config = {"data": data_store}

    assert rule.validate(config) is True
    assert rule._errors.count() == 0
    data_store.instances_by_klass.assert_called_once_with("Timing")


def test_validate_invalid_timing(rule):
    """Test validation with valid timeline exit reference"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "t1",
            "instanceType": "Timing",
            "type": {"decode": "Fixed Reference"},
            "windowLower": "1",
        },
        {
            "id": "t2",
            "instanceType": "Timing",
            "type": {"decode": "Fixed Reference"},
            "windowUpper": "2",
        },
        {
            "id": "t3",
            "instanceType": "Timing",
            "type": {"decode": "Fixed Reference"},
            "windowLower": "1",
            "windowUpper": "2",
        },
    ]
    data_store.path_by_id.side_effect = [
        "root.path1",
        "root.path2",
        "root.path3",
        "root.path4",
    ]

    config = {"data": data_store}

    assert rule.validate(config) is False
    assert rule._errors.count() == 4
    assert rule._errors._items[0].to_dict() == {
        "location": {
            "klass": "Timing",
            "attribute": "windowLower",
            "path": "root.path1",
            "rule": "DDF00025",
            "rule_text": "A window must not be defined for an anchor timing (i.e., type is "
            + '"Fixed Reference").',
        },
        "message": "Window lower defined for anchor timing",
        "level": "Error",
    }
    assert rule._errors._items[1].to_dict() == {
        "location": {
            "klass": "Timing",
            "attribute": "windowUpper",
            "path": "root.path2",
            "rule": "DDF00025",
            "rule_text": "A window must not be defined for an anchor timing (i.e., type is "
            + '"Fixed Reference").',
        },
        "message": "Window upper defined for anchor timing",
        "level": "Error",
    }
    assert rule._errors._items[2].to_dict() == {
        "location": {
            "klass": "Timing",
            "attribute": "windowLower",
            "path": "root.path3",
            "rule": "DDF00025",
            "rule_text": "A window must not be defined for an anchor timing (i.e., type is "
            + '"Fixed Reference").',
        },
        "message": "Window lower defined for anchor timing",
        "level": "Error",
    }
    assert rule._errors._items[3].to_dict() == {
        "location": {
            "klass": "Timing",
            "attribute": "windowUpper",
            "path": "root.path4",
            "rule": "DDF00025",
            "rule_text": "A window must not be defined for an anchor timing (i.e., type is "
            + '"Fixed Reference").',
        },
        "message": "Window upper defined for anchor timing",
        "level": "Error",
    }
