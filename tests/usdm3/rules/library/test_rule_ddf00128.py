import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00128 import RuleDDF00128

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00128 instance"""
    return RuleDDF00128()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00128"
    assert rule.level == rule.WARNING
    assert rule.description == "A study intervention's type must be specified using the Intervention Type Response (C99078) SDTM codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

