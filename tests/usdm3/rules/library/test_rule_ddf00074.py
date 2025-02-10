import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00074 import RuleDDF00074

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00074 instance"""
    return RuleDDF00074()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00074"
    assert rule.level == rule.WARNING
    assert rule.description == "If the intervention model indicates a single group design then only one intervention is expected. In all other cases more interventions are expected."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

