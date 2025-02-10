import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00013 import RuleDDF00013

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00013 instance"""
    return RuleDDF00013()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00013"
    assert rule.level == rule.WARNING
    assert rule.description == "If a biomedical concept property is required then it must also be enabled, while if it is not enabled then it must not be required."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

