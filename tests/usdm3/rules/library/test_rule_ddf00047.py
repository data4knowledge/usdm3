import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00047 import RuleDDF00047

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00047 instance"""
    return RuleDDF00047()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00047"
    assert rule.level == rule.WARNING
    assert rule.description == "A study cell must only reference elements that are defined within the same study design as the study cell."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

