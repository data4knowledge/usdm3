import pytest
from usdm3.rules.library.rule_ddf00026 import RuleDDF00026
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00026()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00026"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == 'A scheduled activity instance must not point (via the "timeline" relationship) to the timeline in which it is specified.'
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
