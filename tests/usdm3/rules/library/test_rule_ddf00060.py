import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00060 import RuleDDF00060

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00060 instance"""
    return RuleDDF00060()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00060"
    assert rule.level == rule.WARNING
    assert rule.description == "The value for each timing must be a non-negative duration specified in ISO 8601 format."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

