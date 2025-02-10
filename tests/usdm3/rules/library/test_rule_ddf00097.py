import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00097 import RuleDDF00097

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00097 instance"""
    return RuleDDF00097()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00097"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design, the planned age range must be specified either in the study population or in all cohorts."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

