import pytest
from usdm3.rules.library.rule_ddf00149 import RuleDDF00149
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00149()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00149"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A study arm data origin type must be specified according to the extensible data origin type (C188727) DDF codelist (e.g. an entry with a code or decode used from the codelist should be consistent with the full entry in the codelist)."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
