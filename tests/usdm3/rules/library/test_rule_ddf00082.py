import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00082 import RuleDDF00082

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00082 instance"""
    return RuleDDF00082()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00082"
    assert rule.level == rule.WARNING
    assert rule.description == "Data types of attributes (string, number, boolean) must conform with the USDM schema based on the API specification."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

