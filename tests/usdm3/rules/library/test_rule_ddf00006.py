import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00006 import RuleDDF00006
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00006 instance"""
    rule = "DDF00006"
    level = RuleTemplate.WARNING
    description = "Timing windows must be fully defined, if one of the window attributes (i.e., window label, window lower, and window upper) is defined then all must be specified."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00006"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "Timing windows must be fully defined, if one of the window attributes (i.e., window label, window lower, and window upper) is defined then all must be specified."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

