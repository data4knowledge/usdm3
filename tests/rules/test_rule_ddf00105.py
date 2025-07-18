import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00105 import RuleDDF00105
from usdm3.rules.library.rule_template import RuleTemplate
from tests.helpers.rule_error import error_timestamp


@pytest.fixture
def rule():
    return RuleDDF00105()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00105"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance."
    )
    assert rule._errors.count() == 0


def test_validate_epoch_in_different_study_design(rule):
    data_store = Mock()
    data_store.instances_by_klass.side_effect = [
        [
            {
                "id": "sai1",
                "epochId": "ep1",
                "instanceType": "ScheduledActivityInstance",
            }
        ],
        [
            {
                "id": "sdi1",
                "epochId": "ep2",
                "instanceType": "ScheduledDecisionInstance",
            }
        ],
    ]
    data_store.instance_by_id.side_effect = [
        {
            "id": " ep1",
        },
        {
            "id": "ep2",
        },
    ]
    data_store.parent_by_klass.side_effect = [
        {"id": "sd1"},
        {"id": "sd2"},
        {"id": "sd3"},
        {"id": "sd3"},
    ]
    data_store.path_by_id.side_effect = ["path/path1", "path/path2"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "epochId",
            "klass": "ScheduledActivityInstance",
            "path": "path/path1",
            "rule": "DDF00105",
            "rule_text": "A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance.",
        },
        "message": "Epoch defined in a different study design",
        "type": "DDF00105",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }


def test_validate_epoch_in_same_study_design(rule):
    data_store = Mock()
    data_store.instances_by_klass.side_effect = [
        [
            {
                "id": "sai1",
                "epochId": "ep1",
                "instanceType": "ScheduledActivityInstance",
            }
        ],
        [
            {
                "id": "sdi1",
                "epochId": "ep2",
                "instanceType": "ScheduledDecisionInstance",
            }
        ],
    ]
    data_store.instance_by_id.side_effect = [
        {
            "id": " ep1",
        },
        {
            "id": "ep2",
        },
    ]
    data_store.parent_by_klass.side_effect = [
        {"id": "sd1"},
        {"id": "sd1"},
        {"id": "sd3"},
        {"id": "sd3"},
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}
    assert rule.validate(config) is True
    assert rule._errors.count() == 0


def test_validate_epoch_both_missing(rule):
    data_store = Mock()
    data_store.instances_by_klass.side_effect = [
        [
            {
                "id": "sai1",
                "epochId": "ep1",
                "instanceType": "ScheduledActivityInstance",
            }
        ],
        [
            {
                "id": "sdi1",
                "epochId": "ep2",
                "instanceType": "ScheduledDecisionInstance",
            }
        ],
    ]
    data_store.instance_by_id.side_effect = [
        {"id": " ep1", "instanceType": "XXX"},
        {"id": "ep2", "instanceType": "YYY"},
    ]
    data_store.parent_by_klass.side_effect = [None, None, None, None]
    data_store.path_by_id.side_effect = ["path/path1", "path/path2"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 2
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "epochId",
            "klass": "ScheduledActivityInstance",
            "path": "path/path1",
            "rule": "DDF00105",
            "rule_text": "A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance.",
        },
        "message": "ScheduledActivityInstance and XXX missing parents",
        "type": "DDF00105",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }
    assert error_timestamp(rule._errors, 1) == {
        "level": "Error",
        "location": {
            "attribute": "epochId",
            "klass": "ScheduledDecisionInstance",
            "path": "path/path2",
            "rule": "DDF00105",
            "rule_text": "A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance.",
        },
        "message": "ScheduledDecisionInstance and YYY missing parents",
        "type": "DDF00105",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }


def test_validate_epoch_first_missing(rule):
    data_store = Mock()
    data_store.instances_by_klass.side_effect = [
        [
            {
                "id": "sai1",
                "epochId": "ep1",
                "instanceType": "ScheduledActivityInstance",
            }
        ],
        [
            {
                "id": "sdi1",
                "epochId": "ep2",
                "instanceType": "ScheduledDecisionInstance",
            }
        ],
    ]
    data_store.instance_by_id.side_effect = [
        {"id": " ep1", "instanceType": "XXX"},
        {"id": "ep2", "instanceType": "YYY"},
    ]
    data_store.parent_by_klass.side_effect = [
        None,
        {"id": "sd2"},
        {"id": "sd3"},
        {"id": "sd3"},
    ]
    data_store.path_by_id.side_effect = ["path/path1", "path/path2"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "epochId",
            "klass": "ScheduledActivityInstance",
            "path": "path/path1",
            "rule": "DDF00105",
            "rule_text": "A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance.",
        },
        "message": "ScheduledActivityInstance missing parent",
        "type": "DDF00105",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }


def test_validate_epoch_second_missing(rule):
    data_store = Mock()
    data_store.instances_by_klass.side_effect = [
        [
            {
                "id": "sai1",
                "epochId": "ep1",
                "instanceType": "ScheduledActivityInstance",
            },
        ],
        [],
    ]
    data_store.instance_by_id.side_effect = [
        {"id": " ep1", "instanceType": "XXX"},
        {"id": "ep2", "instanceType": "YYY"},
    ]
    data_store.parent_by_klass.side_effect = [
        {"id": "sd2"},
        None,
        {"id": "sd3"},
        {"id": "sd4"},
    ]
    data_store.path_by_id.side_effect = ["path/path1", "path/path2"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "epochId",
            "klass": "ScheduledActivityInstance",
            "path": "path/path1",
            "rule": "DDF00105",
            "rule_text": "A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance.",
        },
        "message": "XXX missing parent",
        "type": "DDF00105",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }
