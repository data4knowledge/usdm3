import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00016 import RuleDDF00016
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00016 instance"""
    rule = "DDF00016"
    level = RuleTemplate.WARNING
    description = "A specified condition for assessments must apply to at least to a procedure, biomedical concept, biomedical concept surrogate, biomedical concept category or a whole activity."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00016"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A specified condition for assessments must apply to at least to a procedure, biomedical concept, biomedical concept surrogate, biomedical concept category or a whole activity."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
