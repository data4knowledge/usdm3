import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00100 import RuleDDF00100

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00100 instance"""
    return RuleDDF00100()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00100"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study version, there must be no more than one title of each type."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

