import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00108 import RuleDDF00108
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00108 instance"""
    rule = "DDF00108"
    level = RuleTemplate.WARNING
    description = "There must be at least one exit defined for each timeline (i.e., at least one instance of StudyTimelineExit linked via the 'exits' relationship)."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00108"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "There must be at least one exit defined for each timeline (i.e., at least one instance of StudyTimelineExit linked via the 'exits' relationship)."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

