import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00110 import RuleDDF00110

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00110 instance"""
    return RuleDDF00110()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00110"
    assert rule.level == rule.WARNING
    assert rule.description == "An eligibility criterion's category must be specified using the Category of Inclusion/Exclusion (C66797) SDTM codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

