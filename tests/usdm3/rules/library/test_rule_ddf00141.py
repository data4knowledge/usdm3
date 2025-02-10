import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00141 import RuleDDF00141

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00141 instance"""
    return RuleDDF00141()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00141"
    assert rule.level == rule.WARNING
    assert rule.description == "A planned sex must be specified using the Sex of Participants (C66732) SDTM codelist."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

