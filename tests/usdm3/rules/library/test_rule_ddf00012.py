import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00012 import RuleDDF00012

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00012 instance"""
    return RuleDDF00012()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00012"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design, there must be exactly one scheduled timeline which identifies as the main Timeline."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

