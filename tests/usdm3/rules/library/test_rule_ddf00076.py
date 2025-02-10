import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00076 import RuleDDF00076

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00076 instance"""
    return RuleDDF00076()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00076"
    assert rule.level == rule.WARNING
    assert rule.description == "If a biomedical concept is referenced from an activity then it is not expected to be referenced as well by a biomedical concept category that is referenced from the same activity."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

