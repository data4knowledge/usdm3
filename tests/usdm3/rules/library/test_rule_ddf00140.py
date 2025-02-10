import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00140 import RuleDDF00140

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00140 instance"""
    return RuleDDF00140()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00140"
    assert rule.level == rule.WARNING
    assert rule.description == "An organization type must be specified according to the extensible organization type (C188724) DDF codelist (e.g. an entry with a code or decode used from the codelist should be consistent with the full entry in the codelist)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

