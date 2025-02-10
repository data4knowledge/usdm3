import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00016 import RuleDDF00016

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00016 instance"""
    return RuleDDF00016()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00016"
    assert rule.level == rule.WARNING
    assert rule.description == "A specified condition for assessments must apply to at least to a procedure, biomedical concept, biomedical concept surrogate, biomedical concept category or a whole activity."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

