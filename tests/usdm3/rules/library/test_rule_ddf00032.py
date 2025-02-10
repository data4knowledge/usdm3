import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00032 import RuleDDF00032

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00032 instance"""
    return RuleDDF00032()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00032"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study version, if more than 1 business therapeutic area is defined then they must be distinct."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

