import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00005 import RuleDDF00005

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00005 instance"""
    return RuleDDF00005()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00005"
    assert rule.level == rule.WARNING
    assert rule.description == "Every study version must have exactly one study identifier with an identifier scope that references a clinical study sponsor organization."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

