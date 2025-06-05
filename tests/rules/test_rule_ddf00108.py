import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00108 import RuleDDF00108
from usdm3.rules.library.rule_template import RuleTemplate
from tests.helpers.rule_error import error_timestamp


@pytest.fixture
def rule():
    return RuleDDF00108()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00108"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "There must be at least one exit defined for each timeline (i.e., at least one instance of StudyTimelineExit linked via the 'exits' relationship)."
    )
    assert rule._errors.count() == 0


def test_validate_valid(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "code1",
            "exits": ["id1", "id2"],
        },
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}
    assert rule.validate(config) is True
    assert rule._errors.count() == 0


def test_validate_no_exits(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "code1",
            "exits": [],
        },
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "exits",
            "klass": "StudyTimeline",
            "path": "path/path1",
            "rule": "DDF00108",
            "rule_text": "There must be at least one exit defined for each timeline (i.e., at least one instance of StudyTimelineExit linked via the 'exits' relationship).",
        },
        "message": "No exits defined for timeline",
        "type": "DDF00108",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }


def test_validate_missing_exits(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "code1",
        },
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "exits",
            "klass": "StudyTimeline",
            "path": "path/path1",
            "rule": "DDF00108",
            "rule_text": "There must be at least one exit defined for each timeline (i.e., at least one instance of StudyTimelineExit linked via the 'exits' relationship).",
        },
        "message": "Missing exits",
        "type": "DDF00108",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }
