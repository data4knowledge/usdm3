import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00116 import RuleDDF00116

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00116 instance"""
    return RuleDDF00116()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00116"
    assert rule.level == rule.WARNING
    assert rule.description == "A study version's study type must be specified using the Study Type Response (C99077) SDTM codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

