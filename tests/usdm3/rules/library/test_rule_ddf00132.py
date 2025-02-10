import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00132 import RuleDDF00132

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00132 instance"""
    return RuleDDF00132()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00132"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design, if a planned completion number is defined, it must be specified either in the study population or in all cohorts."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

