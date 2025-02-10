import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00027 import RuleDDF00027

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00027 instance"""
    return RuleDDF00027()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00027"
    assert rule.level == rule.WARNING
    assert rule.description == "To ensure consistent ordering, the same instance must not be referenced more than once as previous or next."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

