import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00040 import RuleDDF00040

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00040 instance"""
    return RuleDDF00040()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00040"
    assert rule.level == rule.WARNING
    assert rule.description == "Each study element must be referenced by at least one study cell."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

