import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00007 import RuleDDF00007

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00007 instance"""
    return RuleDDF00007()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00007"
    assert rule.level == rule.WARNING
    assert rule.description == "If timing type is "Fixed Reference" then it must point to only one scheduled instance (e.g. attribute relativeToScheduledInstance must be equal to relativeFromScheduledInstance or it must be missing)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

