import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00075 import RuleDDF00075

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00075 instance"""
    return RuleDDF00075()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00075"
    assert rule.level == rule.WARNING
    assert rule.description == "An activity is expected to refer to at least one procedure, biomedical concept, biomedical concept category or biomedical concept surrogate."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

