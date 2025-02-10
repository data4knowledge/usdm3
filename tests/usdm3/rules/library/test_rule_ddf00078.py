import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00078 import RuleDDF00078

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00078 instance"""
    return RuleDDF00078()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00078"
    assert rule.level == rule.WARNING
    assert rule.description == "If a transition start rule is defined then an end rule is expected and vice versa."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

