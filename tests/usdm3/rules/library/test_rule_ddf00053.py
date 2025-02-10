import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00053 import RuleDDF00053

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00053 instance"""
    return RuleDDF00053()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00053"
    assert rule.level == rule.WARNING
    assert rule.description == "Within an encounter there must be no duplicate environmental settings."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

