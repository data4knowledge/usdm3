import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00111 import RuleDDF00111

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00111 instance"""
    return RuleDDF00111()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00111"
    assert rule.level == rule.WARNING
    assert rule.description == "The unit of a planned age is expected to be specified using terms from the Age Unit (C66781) SDTM codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

