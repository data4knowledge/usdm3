import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00055 import RuleDDF00055

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00055 instance"""
    return RuleDDF00055()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00055"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study design, if more trial types are defined, they must be distinct."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

