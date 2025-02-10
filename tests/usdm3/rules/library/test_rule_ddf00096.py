import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00096 import RuleDDF00096

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00096 instance"""
    return RuleDDF00096()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00096"
    assert rule.level == rule.WARNING
    assert rule.description == "All primary endpoints must be referenced by a primary objective."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

