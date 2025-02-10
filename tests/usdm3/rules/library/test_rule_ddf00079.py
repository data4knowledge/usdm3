import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00079 import RuleDDF00079

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00079 instance"""
    return RuleDDF00079()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00079"
    assert rule.level == rule.WARNING
    assert rule.description == "If a synonym is specified then it is not expected to be equal to the name of the biomedical concept (case insensitive)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

