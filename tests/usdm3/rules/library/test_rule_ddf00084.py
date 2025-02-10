import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00084 import RuleDDF00084

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00084 instance"""
    return RuleDDF00084()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00084"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design there must be exactly one objective with level 'Primary Objective'."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

