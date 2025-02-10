import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00114 import RuleDDF00114

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00114 instance"""
    return RuleDDF00114()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00114"
    assert rule.level == rule.WARNING
    assert rule.description == "If specified, the context of a condition must point to a valid instance in the activity or scheduled activity instance class."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

