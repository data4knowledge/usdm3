import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00041 import RuleDDF00041

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00041 instance"""
    return RuleDDF00041()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00041"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design, there must be at least one endpoint with level primary."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

