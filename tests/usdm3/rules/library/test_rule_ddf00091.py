import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00091 import RuleDDF00091

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00091 instance"""
    return RuleDDF00091()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00091"
    assert rule.level == rule.WARNING
    assert rule.description == "When a condition applies to a procedure, activity, biomedical concept, biomedical concept category, or biomedical concept surrogate then an instance must be available in the corresponding class with the specified id."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

