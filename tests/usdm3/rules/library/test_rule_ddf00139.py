import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00139 import RuleDDF00139

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00139 instance"""
    return RuleDDF00139()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00139"
    assert rule.level == rule.WARNING
    assert rule.description == "An identified organization is not expected to have more than one identifier for the study."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

