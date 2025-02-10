import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00046 import RuleDDF00046

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00046 instance"""
    return RuleDDF00046()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00046"
    assert rule.level == rule.WARNING
    assert rule.description == "A timing must only be specified as being relative to/from a scheduled activity/decision instance that is defined within the same timeline as the timing."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

