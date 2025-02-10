import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00037 import RuleDDF00037

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00037 instance"""
    return RuleDDF00037()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00037"
    assert rule.level == rule.WARNING
    assert rule.description == "At least one scheduled activity instance within a timeline must point to a timeline exit."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

