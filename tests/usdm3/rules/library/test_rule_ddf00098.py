import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00098 import RuleDDF00098

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00098 instance"""
    return RuleDDF00098()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00098"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design, the planned sex must be specified either in the study population or in all cohorts."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

