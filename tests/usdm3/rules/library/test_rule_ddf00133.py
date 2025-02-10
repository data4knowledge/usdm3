import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00133 import RuleDDF00133
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00133 instance"""
    rule = "DDF00133"
    level = RuleTemplate.WARNING
    description = "Within a study design, if a planned enrollment number is defined, it must be specified either in the study population or in all cohorts."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00133"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "Within a study design, if a planned enrollment number is defined, it must be specified either in the study population or in all cohorts."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

