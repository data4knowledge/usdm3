import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00009 import RuleDDF00009
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00009()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00009"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Each schedule timeline must contain at least one anchor (fixed time) - i.e., at least one scheduled activity instance that is referenced by a Fixed Reference timing."
    )
    assert rule._errors.count() == 0


def test_validate_valid_timeline_entry(rule):
    """Test validation with valid timeline entry reference"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "si1",
            "instanceType": "ScheduledTimeline",
            "timings": [
                {"type": {"decode": "Fixed Reference"}},
                {"type": {"decode": "Something Else"}},
            ],
        }
    ]
    config = {"data": data_store}
    assert rule.validate(config) is True
    assert rule._errors.count() == 0


def test_validate_invalid_timeline_entry(rule):
    """Test validation with invalid timeline entry reference"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "si1",
            "instanceType": "ScheduledTimeline",
            "timings": [
                {"type": {"decode": "XXX"}},
                {"type": {"decode": "Something Else"}},
            ],
        }
    ]
    data_store.path_by_id.return_value = "root.path1"
    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert rule._errors._items[0].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "timings",
            "klass": "ScheduledTimeline",
            "path": "root.path1",
            "rule": "DDF00009",
            "rule_text": "Each schedule timeline must contain at least one anchor (fixed time) - i.e., at least one scheduled activity instance that is referenced by a Fixed Reference timing.",
        },
        "message": "No fixed reference timing",
    }
