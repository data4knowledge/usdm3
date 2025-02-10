import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00062 import RuleDDF00062

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00062 instance"""
    return RuleDDF00062()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00062"
    assert rule.level == rule.WARNING
    assert rule.description == "When specified, the upper limit of a timing window must be a non-negative duration in ISO 8601 format."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

