import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00146 import RuleDDF00146

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00146 instance"""
    return RuleDDF00146()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00146"
    assert rule.level == rule.WARNING
    assert rule.description == "A study title type must be specified using the study title type (C207419) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

