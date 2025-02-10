import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00043 import RuleDDF00043

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00043 instance"""
    return RuleDDF00043()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00043"
    assert rule.level == rule.WARNING
    assert rule.description == "A unit must not be specified for a planned enrollment number or a planned completion number."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

