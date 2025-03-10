import pytest
from usdm3.rules.library.rule_ddf00075 import RuleDDF00075
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00075()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00075"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "An activity is expected to refer to at least one procedure, biomedical concept, biomedical concept category or biomedical concept surrogate."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
