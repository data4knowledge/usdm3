import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00070 import RuleDDF00070

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00070 instance"""
    return RuleDDF00070()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00070"
    assert rule.level == rule.WARNING
    assert rule.description == "The minimum value of a range must be less than or equal to the maximum value of the range."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

