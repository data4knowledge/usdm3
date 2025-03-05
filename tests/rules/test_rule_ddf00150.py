import pytest
from unittest.mock import patch, call
from usdm3.rules.library.rule_ddf00150 import RuleDDF00150
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00150()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00150"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "An encounter type must be specified according to the extensible encounter type (C188728) DDF codelist (e.g. an entry with a code or decode used from the codelist should be consistent with the full entry in the codelist)."
    )
    assert rule._errors.count() == 0


@patch("usdm3.rules.library.rule_template.RuleTemplate._ct_check")
def test_validate(mock_ct_check, rule):
    """Test validate method with ct_check"""
    rule.validate({"data": {}, "ct": {}})
    mock_ct_check.side_effect = [True]
    mock_ct_check.assert_has_calls(
        [
            call({"data": {}, "ct": {}}, "Encounter", "type"),
        ]
    )
