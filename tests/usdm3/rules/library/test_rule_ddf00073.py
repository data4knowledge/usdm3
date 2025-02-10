import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00073 import RuleDDF00073
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00073 instance"""
    rule = "DDF00073"
    level = RuleTemplate.WARNING
    description = "Only one version of any code system is expected to be used within a study version."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00073"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Only one version of any code system is expected to be used within a study version."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
