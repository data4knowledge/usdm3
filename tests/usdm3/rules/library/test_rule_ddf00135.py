import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00135 import RuleDDF00135
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00135 instance"""
    rule = "DDF00135"
    level = RuleTemplate.WARNING
    description = "An encounter's environmental setting must be specified according to the extensible Environmental Setting (C127262) SDTM codelist (e.g. an entry with a code or decode used from the codelist should be consistent with the full entry in the codelist)."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00135"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "An encounter's environmental setting must be specified according to the extensible Environmental Setting (C127262) SDTM codelist (e.g. an entry with a code or decode used from the codelist should be consistent with the full entry in the codelist)."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
