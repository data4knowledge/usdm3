import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00019 import RuleDDF00019

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00019 instance"""
    return RuleDDF00019()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00019"
    assert rule.level == rule.WARNING
    assert rule.description == "A scheduled activity/decision instance must not refer to itself as its default condition."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

