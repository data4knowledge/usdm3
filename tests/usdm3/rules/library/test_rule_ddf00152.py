import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00152 import RuleDDF00152

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00152 instance"""
    return RuleDDF00152()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00152"
    assert rule.level == rule.WARNING
    assert rule.description == "An activity must only reference timelines that are specified within the same study design."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

