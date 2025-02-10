import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00023 import RuleDDF00023

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00023 instance"""
    return RuleDDF00023()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00023"
    assert rule.level == rule.WARNING
    assert rule.description == "To ensure consistent ordering, when both previous and next attributes are available within an entity the previous id value must match the next id value of the referred instance."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

