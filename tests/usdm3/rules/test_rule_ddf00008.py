import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00008 import RuleDDF00008
from usdm3.rules.library.rule_template import RuleTemplate, ValidationLocation


@pytest.fixture
def rule():
    return RuleDDF00008()


def test_init(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00008"
    assert rule._level == RuleTemplate.ERROR
    assert rule._rule_text == "A scheduled activity instance must refer to either a default condition or a timeline exit, but not both."


def test_validate_valid_timeline_exit(rule):
    """Test validation with valid timeline exit reference"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = [{
        "id": "sai1",
        "instanceType": "ScheduledActivityInstance",
        "timelineExitId": "exit1"
    }]
    data_store.instance_by_id.return_value = {"id": "exit1"}  # Mock timeline exit exists
    
    config = {"data": data_store}

    assert rule.validate(config) is True
    assert rule._errors.count() == 0
    data_store.instances_by_klass.assert_called_once_with("ScheduledActivityInstance")


def test_validate_valid_default_condition(rule):
    """Test validation with valid default condition reference"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = [{
        "id": "sai1",
        "instanceType": "ScheduledActivityInstance",
        "defaultConditionId": "cond1"
    }]
    data_store.instance_by_id.return_value = {"id": "cond1"}  # Mock condition exists
    
    config = {"data": data_store}
    
    assert rule.validate(config) is True
    assert rule._errors.count() == 0
    data_store.instances_by_klass.assert_called_once_with("ScheduledActivityInstance")


def test_validate_invalid_both_references(rule):
    """Test validation with both timeline exit and default condition"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = [{
        "id": "sai1",
        "instanceType": "ScheduledActivityInstance",
        "timelineExitId": "exit1",
        "defaultConditionId": "cond1"
    }]
    
    # Mock that both references exist
    def mock_instance_by_id(id):
        if id == "exit1":
            return {"id": "exit1"}
        if id == "cond1":
            return {"id": "cond1"}
        return None
    
    data_store.instance_by_id.side_effect = mock_instance_by_id
    data_store.path_by_id.return_value = "root.path1"

    config = {"data": data_store}
    
    assert rule.validate(config) is False

    assert rule._errors.count() == 1
    assert rule._errors._items[0].to_dict() == {
        'location': {
            "klass": "ScheduledActivityInstance",
            "attribute": "timelineExitId and defaultConditionId",
            'path': 'root.path1',
            'rule': 'DDF00008',
            'rule_text': 'A scheduled activity instance must refer to either a default '
            'condition or a timeline exit, but not both.'
        },
        'message': "Timeline exit and default condition both exist",
        'level': 'Error',
    }



def test_validate_no_references(rule):
    """Test validation with neither timeline exit nor default condition"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = [{
        "id": "sai1",
        "instanceType": "ScheduledActivityInstance"
    }]
    
    config = {"data": data_store}
    
    assert rule.validate(config) is True
    assert rule._errors.count() == 0


def test_validate_empty_data(rule):
    """Test validation with no scheduled activity instances"""
    data_store = Mock()
    data_store.instances_by_klass.return_value = []
    
    config = {"data": data_store}
    
    assert rule.validate(config) is True
    assert rule._errors.count() == 0
    data_store.instances_by_klass.assert_called_once_with("ScheduledActivityInstance")
