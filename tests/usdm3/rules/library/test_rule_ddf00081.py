import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00081 import RuleDDF00081

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00081 instance"""
    return RuleDDF00081()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00081"
    assert rule.level == rule.ERROR
    assert rule.description == "Class relationships must conform with the USDM schema based on the API specification."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

