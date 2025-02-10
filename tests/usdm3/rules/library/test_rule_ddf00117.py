import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00117 import RuleDDF00117

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00117 instance"""
    return RuleDDF00117()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00117"
    assert rule.level == rule.WARNING
    assert rule.description == "A study protocol document version's protocol status must be specified using the Protocol Status Value Set Terminology (C188723) DDF codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

