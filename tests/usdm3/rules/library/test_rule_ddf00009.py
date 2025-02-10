import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00009 import RuleDDF00009

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00009 instance"""
    return RuleDDF00009()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00009"
    assert rule.level == rule.WARNING
    assert rule.description == "Each schedule timeline must contain at least one anchor (fixed time) - i.e., at least one scheduled activity instance that is referenced by a Fixed Reference timing."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

