import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00004 import RuleDDF00004

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00004 instance"""
    return RuleDDF00004()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00004"
    assert rule.level == rule.WARNING
    assert rule.description == "If duration will vary (attribute durationWillVary is True) then a reason (attribute reasonDurationWillVary) must be given and vice versa."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

