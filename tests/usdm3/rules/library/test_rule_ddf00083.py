import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00083 import RuleDDF00083

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00083 instance"""
    return RuleDDF00083()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00083"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study version, all id values must be unique."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

