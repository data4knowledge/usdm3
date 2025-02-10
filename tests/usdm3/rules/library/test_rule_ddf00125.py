import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00125 import RuleDDF00125

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00125 instance"""
    return RuleDDF00125()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00125"
    assert rule.level == rule.WARNING
    assert rule.description == "Attributes must be included as defined in the USDM schema based on the API specification (i.e., all required properties are present and no additional attributes are present)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

