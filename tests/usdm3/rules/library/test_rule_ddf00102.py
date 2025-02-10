import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00102 import RuleDDF00102

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00102 instance"""
    return RuleDDF00102()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00102"
    assert rule.level == rule.WARNING
    assert rule.description == "A scheduled activity instance must only reference a timeline exit that is defined within the same schedule timeline as the scheduled activity instance."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

