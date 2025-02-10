import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00049 import RuleDDF00049

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00049 instance"""
    return RuleDDF00049()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00049"
    assert rule.level == rule.WARNING
    assert rule.description == "A study arm must only reference populations that are defined within the same study design as the study arm."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

