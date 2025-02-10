import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00042 import RuleDDF00042

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00042 instance"""
    return RuleDDF00042()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00042"
    assert rule.level == rule.WARNING
    assert rule.description == "The range specified for a planned age is not expected to be approximate."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

