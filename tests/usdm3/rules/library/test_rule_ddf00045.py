import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00045 import RuleDDF00045

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00045 instance"""
    return RuleDDF00045()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00045"
    assert rule.level == rule.WARNING
    assert rule.description == "At least one attribute must be specified for an address."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

