import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00148 import RuleDDF00148

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00148 instance"""
    return RuleDDF00148()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00148"
    assert rule.level == rule.WARNING
    assert rule.description == "An endpoint level must be specified using the endpoint level (C188726) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

