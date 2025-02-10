import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00018 import RuleDDF00018

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00018 instance"""
    return RuleDDF00018()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00018"
    assert rule.level == rule.WARNING
    assert rule.description == "An instance of a class must not reference itself as one of its own children."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

