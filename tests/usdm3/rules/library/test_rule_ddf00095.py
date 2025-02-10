import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00095 import RuleDDF00095

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00095 instance"""
    return RuleDDF00095()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00095"
    assert rule.level == rule.WARNING
    assert rule.description == "Within a study protocol document version, if a date of a specific type exists with a global geographic scope then no other dates are expected with the same type."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

