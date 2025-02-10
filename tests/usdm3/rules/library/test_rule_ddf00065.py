import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00065 import RuleDDF00065

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00065 instance"""
    return RuleDDF00065()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00065"
    assert rule.level == rule.WARNING
    assert rule.description == "A scheduled decision instance is not expected to have a sub-timeline."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

