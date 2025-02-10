import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00086 import RuleDDF00086

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00086 instance"""
    return RuleDDF00086()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00086"
    assert rule.level == rule.WARNING
    assert rule.description == "Syntax template text is expected to be HTML formatted."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

