import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00103 import RuleDDF00103

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00103 instance"""
    return RuleDDF00103()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00103"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a document version, the specified section numbers for narrative content must be unique."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

