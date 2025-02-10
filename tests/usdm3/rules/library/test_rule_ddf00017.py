import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00017 import RuleDDF00017

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00017 instance"""
    return RuleDDF00017()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00017"
    assert rule.level == rule.WARNING
    assert rule.description == "Within subject enrollment, the quantity must be a number or a percentage (i.e. the unit must be empty or %)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

