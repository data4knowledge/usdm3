import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00104 import RuleDDF00104

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00104 instance"""
    return RuleDDF00104()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00104"
    assert rule.level == rule.WARNING
    assert rule.description == "A timing's relative to/from property must be specified using the Timing Relative To From Value Set Terminology (C201265) SDTM codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

