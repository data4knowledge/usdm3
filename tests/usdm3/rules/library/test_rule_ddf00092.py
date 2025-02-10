import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00092 import RuleDDF00092

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00092 instance"""
    return RuleDDF00092()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00092"
    assert rule.level == rule.WARNING
    assert rule.description == "Date values associated to a study protocol document version must be unique regarding the combination of type and geographic scopes of the date."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

