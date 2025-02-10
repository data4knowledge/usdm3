import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00010 import RuleDDF00010

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00010 instance"""
    return RuleDDF00010()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00010"
    assert rule.level == rule.WARNING
    assert rule.description == "The names of all child instances of the same parent class must be unique."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

