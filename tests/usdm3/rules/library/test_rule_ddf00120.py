import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00120 import RuleDDF00120

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00120 instance"""
    return RuleDDF00120()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00120"
    assert rule.level == rule.WARNING
    assert rule.description == "A study design's intervention model must be specified according to the extensible Intervention Model Response (C99076) SDTM codelist (e.g. an entry with a code or decode used from the codelist should be consistent with the full entry in the codelist)."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

