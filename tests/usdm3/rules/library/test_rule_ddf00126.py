import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00126 import RuleDDF00126

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00126 instance"""
    return RuleDDF00126()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00126"
    assert rule.level == rule.WARNING
    assert rule.description == "Cardinalities must be as defined in the USDM schema based on the API specification (i.e., required properties have at least one value and single-value properties are not lists)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

