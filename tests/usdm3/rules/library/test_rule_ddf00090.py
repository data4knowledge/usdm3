import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00090 import RuleDDF00090

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00090 instance"""
    return RuleDDF00090()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00090"
    assert rule.level == rule.WARNING
    assert rule.description == "The same Biomedical Concept Category must not be referenced more than once from the same activity."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

