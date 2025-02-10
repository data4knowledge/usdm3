import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00143 import RuleDDF00143

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00143 instance"""
    return RuleDDF00143()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00143"
    assert rule.level == rule.WARNING
    assert rule.description == "A study amendment reason must be coded using the study amendment reason (C207415) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

