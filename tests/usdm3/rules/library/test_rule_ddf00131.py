import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00131 import RuleDDF00131

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00131 instance"""
    return RuleDDF00131()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00131"
    assert rule.level == rule.WARNING
    assert rule.description == "Referenced items in the narrative content must be available elsewhere in the data model."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

