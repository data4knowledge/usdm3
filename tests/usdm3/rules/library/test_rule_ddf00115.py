import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00115 import RuleDDF00115

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00115 instance"""
    return RuleDDF00115()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00115"
    assert rule.level == rule.WARNING
    assert rule.description == "Every study version must have a title of type "Official Study Title"."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

