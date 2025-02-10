import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00144 import RuleDDF00144

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00144 instance"""
    return RuleDDF00144()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00144"
    assert rule.level == rule.WARNING
    assert rule.description == "A study geographic scope type must be specified using the geographic scope type (C207412) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

