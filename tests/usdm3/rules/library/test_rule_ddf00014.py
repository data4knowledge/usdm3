import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00014 import RuleDDF00014

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00014 instance"""
    return RuleDDF00014()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00014"
    assert rule.level == rule.WARNING
    assert rule.description == "A biomedical concept category is expected to have at least a member or a child."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

