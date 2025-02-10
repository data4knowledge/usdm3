import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00147 import RuleDDF00147

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00147 instance"""
    return RuleDDF00147()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00147"
    assert rule.level == rule.WARNING
    assert rule.description == "An objective level must be specified using the objective level (C188725) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

