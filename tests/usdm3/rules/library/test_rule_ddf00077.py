import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00077 import RuleDDF00077

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00077 instance"""
    return RuleDDF00077()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00077"
    assert rule.level == rule.WARNING
    assert rule.description == "If geographic scope type is global then no codes are expected to specify the specific area within scope while if it is not global then at least one code is expected to specify the specific area within scope."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

