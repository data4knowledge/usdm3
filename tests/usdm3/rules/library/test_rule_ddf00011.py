import pytest
from usdm3.rules.library.rule_ddf00011 import RuleDDF00011
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00011()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00011"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == 'Anchor timings (e.g. type is "Fixed Reference") must be related to a scheduled activity instance via a relativeFromScheduledInstance relationship.'
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
