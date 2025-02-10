import pytest
from usdm3.rules.library.rule_ddf00126 import RuleDDF00126
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00126()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00126"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Cardinalities must be as defined in the USDM schema based on the API specification (i.e., required properties have at least one value and single-value properties are not lists)."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
