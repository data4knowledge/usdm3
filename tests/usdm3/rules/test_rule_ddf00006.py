import pytest
from usdm3.rules.library.rule_ddf00006 import RuleDDF00006
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00006()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00006"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Timing windows must be fully defined, if one of the window attributes (i.e., window label, window lower, and window upper) is defined then all must be specified."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
