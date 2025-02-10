import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00021 import RuleDDF00021

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00021 instance"""
    return RuleDDF00021()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00021"
    assert rule.level == rule.WARNING
    assert rule.description == "An instance of a class must not refer to itself as its previous instance."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

