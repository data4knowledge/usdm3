import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00051 import RuleDDF00051

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00051 instance"""
    return RuleDDF00051()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00051"
    assert rule.level == rule.WARNING
    assert rule.description == "A timing's type must be specified using the Timing Type Value Set Terminology (C201264) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

