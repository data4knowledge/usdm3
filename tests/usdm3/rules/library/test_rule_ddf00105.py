import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00105 import RuleDDF00105

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00105 instance"""
    return RuleDDF00105()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00105"
    assert rule.level == rule.WARNING
    assert rule.description == "A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

