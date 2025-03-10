import pytest
from usdm3.rules.library.rule_ddf00124 import RuleDDF00124
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00124()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00124"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Referenced items in a parameter map must be available elsewhere in the data model."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
