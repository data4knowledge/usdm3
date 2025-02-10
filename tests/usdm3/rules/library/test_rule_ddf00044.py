import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00044 import RuleDDF00044

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00044 instance"""
    return RuleDDF00044()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00044"
    assert rule.level == rule.WARNING
    assert rule.description == "The target for a condition must not be equal to its parent."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

