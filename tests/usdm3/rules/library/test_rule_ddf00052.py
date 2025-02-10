import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00052 import RuleDDF00052

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00052 instance"""
    return RuleDDF00052()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00052"
    assert rule.level == rule.WARNING
    assert rule.description == "All standard code aliases referenced by an instance of the alias code class must be unique."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

