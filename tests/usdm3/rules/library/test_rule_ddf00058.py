import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00058 import RuleDDF00058

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00058 instance"""
    return RuleDDF00058()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00058"
    assert rule.level == rule.WARNING
    assert rule.description == "Within an indication, if more indication codes are defined, they must be distinct."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

