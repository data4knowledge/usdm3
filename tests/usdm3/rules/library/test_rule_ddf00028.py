import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00028 import RuleDDF00028

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00028 instance"""
    return RuleDDF00028()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00028"
    assert rule.level == rule.WARNING
    assert rule.description == "An activity must only reference activities that are specified within the same study design."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

