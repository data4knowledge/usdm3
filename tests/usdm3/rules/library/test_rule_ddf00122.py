import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00122 import RuleDDF00122

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00122 instance"""
    return RuleDDF00122()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00122"
    assert rule.level == rule.WARNING
    assert rule.description == "A study design's characteristics must be specified according to the Study design characteristics (C207416) DDF codelist (e.g. an entry with a code or decode used from the codelist should be consistent with the full entry in the codelist)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

