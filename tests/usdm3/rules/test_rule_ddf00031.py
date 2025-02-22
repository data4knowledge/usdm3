import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00031 import RuleDDF00031
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00031()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00031"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == 'If timing type is not "Fixed Reference" then it must point to two scheduled instances (e.g. the relativeFromScheduledInstance and relativeToScheduledInstance attributes must not be missing and must not be equal to each other).'
    )
    assert rule._errors.count() == 0


def test_validate_valid(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Not Fixed Reference"},
            "instanceType": "Timing",
            "relativeToScheduledInstance": "instance1",
            "relativeFromScheduledInstance": "instance2",
        }
    ]
    data_store.instance_by_id.return_value = {"id": "instance1"}

    config = {"data": data_store}

    assert rule.validate(config) is True
    assert rule._errors.count() == 0


def test_validate_invalid_both_references(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Not Fixed Reference"},
            "instanceType": "Timing",
        }
    ]
    data_store.path_by_id.side_effect = ["path/path1", "path/path2"]

    config = {"data": data_store}

    assert rule.validate(config) is False
    assert rule._errors.count() == 2
    assert rule._errors._items[0].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "relativeToScheduledInstance",
            "klass": "Timing",
            "path": "path/path1",
            "rule": "DDF00031",
            "rule_text": 'If timing type is not "Fixed Reference" then it must point to two '
            "scheduled instances (e.g. the relativeFromScheduledInstance and "
            "relativeToScheduledInstance attributes must not be missing and must "
            "not be equal to each other).",
        },
        "message": "Missing relativeToScheduledInstance",
    }
    assert rule._errors._items[1].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "relativeFromScheduledInstance",
            "klass": "Timing",
            "path": "path/path2",
            "rule": "DDF00031",
            "rule_text": 'If timing type is not "Fixed Reference" then it must point to two '
            "scheduled instances (e.g. the relativeFromScheduledInstance and "
            "relativeToScheduledInstance attributes must not be missing and must "
            "not be equal to each other).",
        },
        "message": "Missing relativeFromScheduledInstance",
    }


def test_validate_invalid_from_references(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Not Fixed Reference"},
            "relativeToScheduledInstance": "instance1",
            "instanceType": "Timing",
        }
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}

    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert rule._errors._items[0].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "relativeFromScheduledInstance",
            "klass": "Timing",
            "path": "path/path1",
            "rule": "DDF00031",
            "rule_text": 'If timing type is not "Fixed Reference" then it must point to two '
            "scheduled instances (e.g. the relativeFromScheduledInstance and "
            "relativeToScheduledInstance attributes must not be missing and must "
            "not be equal to each other).",
        },
        "message": "Missing relativeFromScheduledInstance",
    }


def test_validate_invalid_to_references(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Not Fixed Reference"},
            "relativeToScheduledInstance": "instance1",
            "instanceType": "Timing",
        }
    ]
    data_store.path_by_id.side_effect = ["path/path1", "path/path2"]

    config = {"data": data_store}

    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert rule._errors._items[0].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "relativeFromScheduledInstance",
            "klass": "Timing",
            "path": "path/path1",
            "rule": "DDF00031",
            "rule_text": 'If timing type is not "Fixed Reference" then it must point to two '
            "scheduled instances (e.g. the relativeFromScheduledInstance and "
            "relativeToScheduledInstance attributes must not be missing and must "
            "not be equal to each other).",
        },
        "message": "Missing relativeFromScheduledInstance",
    }


def test_validate_empty_data(rule):
    """Test validation with no timing instances"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = []

    config = {"data": data_store}

    assert rule.validate(config) is True
    assert rule._errors.count() == 0
