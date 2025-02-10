import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00085 import RuleDDF00085

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00085 instance"""
    return RuleDDF00085()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00085"
    assert rule.level == rule.WARNING
    assert rule.description == "Narrative content text is expected to be HTML formatted."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

