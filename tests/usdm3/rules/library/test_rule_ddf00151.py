import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00151 import RuleDDF00151

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00151 instance"""
    return RuleDDF00151()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00151"
    assert rule.level == rule.WARNING
    assert rule.description == "If geographic scope type is global then there must be only one geographic scope specified."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

