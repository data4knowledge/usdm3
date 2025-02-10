import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00080 import RuleDDF00080

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00080 instance"""
    return RuleDDF00080()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00080"
    assert rule.level == rule.WARNING
    assert rule.description == "All scheduled activity instances are expected to refer to an epoch."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

