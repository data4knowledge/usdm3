import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00006 import RuleDDF00006

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00006 instance"""
    return RuleDDF00006()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00006"
    assert rule.level == rule.WARNING
    assert rule.description == "Timing windows must be fully defined, if one of the window attributes (i.e., window label, window lower, and window upper) is defined then all must be specified."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

