import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00088 import RuleDDF00088

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00088 instance"""
    return RuleDDF00088()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00088"
    assert rule.level == rule.WARNING
    assert rule.description == "Epoch ordering using previous and next attributes is expected to be consistent with the order of corresponding scheduled activity instances according to their specified default conditions."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

