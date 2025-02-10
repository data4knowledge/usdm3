import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00101 import RuleDDF00101

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00101 instance"""
    return RuleDDF00101()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00101"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design, if study type is Interventional then at least one intervention is expected to be referenced from a procedure."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

