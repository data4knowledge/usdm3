import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00124 import RuleDDF00124

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00124 instance"""
    return RuleDDF00124()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00124"
    assert rule.level == rule.WARNING
    assert rule.description == "Referenced items in a parameter map must be available elsewhere in the data model."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

