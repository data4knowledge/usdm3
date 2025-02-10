import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00133 import RuleDDF00133

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00133 instance"""
    return RuleDDF00133()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00133"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design, if a planned enrollment number is defined, it must be specified either in the study population or in all cohorts."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

