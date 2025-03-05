import pytest
from usdm3.rules.library.rule_ddf00117 import RuleDDF00117
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00117()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00117"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A study protocol document version's protocol status must be specified using the Protocol Status Value Set Terminology (C188723) DDF codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
