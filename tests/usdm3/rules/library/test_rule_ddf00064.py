import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00064 import RuleDDF00064

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00064 instance"""
    return RuleDDF00064()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00064"
    assert rule.level == rule.WARNING
    assert rule.description == "A scheduled decision instance is not expected to refer to a timeline exit."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

