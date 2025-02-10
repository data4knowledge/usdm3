import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00040 import RuleDDF00040
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00040 instance"""
    rule = "DDF00040"
    level = RuleTemplate.WARNING
    description = "Each study element must be referenced by at least one study cell."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00040"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Each study element must be referenced by at least one study cell."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
