import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00026 import RuleDDF00026

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00026 instance"""
    return RuleDDF00026()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00026"
    assert rule.level == rule.WARNING
    assert rule.description == "A scheduled activity instance must not point (via the "timeline" relationship) to the timeline in which it is specified."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

