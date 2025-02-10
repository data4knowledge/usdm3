import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00107 import RuleDDF00107

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00107 instance"""
    return RuleDDF00107()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00107"
    assert rule.level == rule.WARNING
    assert rule.description == "A scheduled activity instance must only have a sub-timeline that is defined within the same study design as the scheduled activity instance."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

