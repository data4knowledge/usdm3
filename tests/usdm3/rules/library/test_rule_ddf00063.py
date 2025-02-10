import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00063 import RuleDDF00063

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00063 instance"""
    return RuleDDF00063()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00063"
    assert rule.level == rule.WARNING
    assert rule.description == "A standard code alias is not expected to be equal to the standard code (e.g. no equal code or decode for the same coding system version is expected)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

