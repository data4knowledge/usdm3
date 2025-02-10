import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00011 import RuleDDF00011

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00011 instance"""
    return RuleDDF00011()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00011"
    assert rule.level == rule.WARNING
    assert rule.description == "Anchor timings (e.g. type is \"Fixed Reference\") must be related to a scheduled activity instance via a relativeFromScheduledInstance relationship."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

