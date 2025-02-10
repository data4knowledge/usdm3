import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00003 import RuleDDF00003

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00003 instance"""
    return RuleDDF00003()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00003"
    assert rule.level == rule.WARNING
    assert rule.description == "If the duration of an administration will vary, a quantity is not expected for the administration duration and vice versa."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

