import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00101 import RuleDDF00101
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00101 instance"""
    rule = "DDF00101"
    level = RuleTemplate.WARNING
    description = "Within a study design, if study type is Interventional then at least one intervention is expected to be referenced from a procedure."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00101"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "Within a study design, if study type is Interventional then at least one intervention is expected to be referenced from a procedure."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

