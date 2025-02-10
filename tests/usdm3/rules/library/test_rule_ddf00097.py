import pytest
from usdm3.rules.library.rule_ddf00097 import RuleDDF00097
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00097()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00097"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Within a study design, the planned age range must be specified either in the study population or in all cohorts."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
