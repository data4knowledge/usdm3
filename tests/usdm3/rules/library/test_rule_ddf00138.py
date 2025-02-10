import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00138 import RuleDDF00138

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00138 instance"""
    return RuleDDF00138()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00138"
    assert rule.level == rule.WARNING
    assert rule.description == "Every identifier must be unique within the scope of an identified organization."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

