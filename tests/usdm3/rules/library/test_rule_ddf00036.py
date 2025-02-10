import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00036 import RuleDDF00036

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00036 instance"""
    return RuleDDF00036()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00036"
    assert rule.level == rule.WARNING
    assert rule.description == "If timing type is "Fixed Reference" then the corresponding attribute relativeToFrom must be filled with "Start to Start"."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

