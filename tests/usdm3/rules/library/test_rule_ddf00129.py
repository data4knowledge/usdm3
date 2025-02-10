import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00129 import RuleDDF00129

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00129 instance"""
    return RuleDDF00129()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00129"
    assert rule.level == rule.WARNING
    assert rule.description == "A study intervention's product designation must be specified using the product designation (C207418) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

