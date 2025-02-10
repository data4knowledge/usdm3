import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00127 import RuleDDF00127

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00127 instance"""
    return RuleDDF00127()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00127"
    assert rule.level == rule.WARNING
    assert rule.description == "An encounter must only be scheduled at a timing that is defined within the same study design as the encounter."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

