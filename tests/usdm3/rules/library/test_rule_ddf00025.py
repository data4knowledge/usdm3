import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00025 import RuleDDF00025

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00025 instance"""
    return RuleDDF00025()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00025"
    assert rule.level == rule.WARNING
    assert rule.description == "A window must not be defined for an anchor timing (i.e., type is "Fixed Reference")."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

