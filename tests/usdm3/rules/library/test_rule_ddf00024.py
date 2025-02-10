import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00024 import RuleDDF00024

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00024 instance"""
    return RuleDDF00024()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00024"
    assert rule.level == rule.WARNING
    assert rule.description == "An epoch must only reference epochs that are specified within the same study design."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

