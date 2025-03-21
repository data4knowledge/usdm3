import pytest
from usdm3.rules.library.rule_ddf00102 import RuleDDF00102
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00102()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00102"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A scheduled activity instance must only reference a timeline exit that is defined within the same schedule timeline as the scheduled activity instance."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
