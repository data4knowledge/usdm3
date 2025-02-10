import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00155 import RuleDDF00155

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00155 instance"""
    return RuleDDF00155()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00155"
    assert rule.level == rule.WARNING
    assert rule.description == "For CDISC codelist references (where the code system is 'http://www.cdisc.org'), the code system version must be a valid CDISC terminology release date in ISO 8601 date format."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

