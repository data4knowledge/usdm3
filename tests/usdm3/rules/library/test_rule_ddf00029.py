import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00029 import RuleDDF00029

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00029 instance"""
    return RuleDDF00029()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00029"
    assert rule.level == rule.WARNING
    assert rule.description == "An encounter must only reference encounters that are specified within the same study design."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

