import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00089 import RuleDDF00089

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00089 instance"""
    return RuleDDF00089()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00089"
    assert rule.level == rule.WARNING
    assert rule.description == "Any parameter name referenced in a tag in the text should be specified in the data dictionary parameter maps."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

