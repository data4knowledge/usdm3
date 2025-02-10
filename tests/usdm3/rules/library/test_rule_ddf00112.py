import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00112 import RuleDDF00112

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00112 instance"""
    return RuleDDF00112()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00112"
    assert rule.level == rule.WARNING
    assert rule.description == "A study intervention's role must be specified using the study intervention role (C207417) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

