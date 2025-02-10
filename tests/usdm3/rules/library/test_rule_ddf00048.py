import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00048 import RuleDDF00048

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00048 instance"""
    return RuleDDF00048()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00048"
    assert rule.level == rule.WARNING
    assert rule.description == "A procedure must only reference a study intervention that is defined within the same study design as the activity within which the procedure is defined."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

