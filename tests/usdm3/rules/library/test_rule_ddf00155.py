import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00155 instance"""
    rule = "DDF00155"
    level = RuleTemplate.WARNING
    description = "For CDISC codelist references (where the code system is 'http://www.cdisc.org'), the code system version must be a valid CDISC terminology release date in ISO 8601 date format."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00155"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "For CDISC codelist references (where the code system is 'http://www.cdisc.org'), the code system version must be a valid CDISC terminology release date in ISO 8601 date format."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
