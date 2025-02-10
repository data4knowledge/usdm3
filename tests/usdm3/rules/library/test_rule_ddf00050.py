import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00050 import RuleDDF00050

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00050 instance"""
    return RuleDDF00050()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00050"
    assert rule.level == rule.WARNING
    assert rule.description == "A study arm must only reference study populations or cohorts that are defined within the same study design as the study arm."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

