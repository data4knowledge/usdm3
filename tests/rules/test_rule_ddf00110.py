import pytest
from usdm3.rules.library.rule_ddf00110 import RuleDDF00110
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00110()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00110"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "An eligibility criterion's category must be specified using the Category of Inclusion/Exclusion (C66797) SDTM codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
