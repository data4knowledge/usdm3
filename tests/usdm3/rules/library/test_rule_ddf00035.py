import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00035 import RuleDDF00035

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00035 instance"""
    return RuleDDF00035()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00035"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a code system and corresponding version, a one-to-one relationship between code and decode is expected."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

