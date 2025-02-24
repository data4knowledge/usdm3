import pytest
from unittest.mock import patch, call
from usdm3.rules.library.rule_ddf00141 import RuleDDF00141
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00141()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00141"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A planned sex must be specified using the Sex of Participants (C66732) SDTM codelist."
    )
    assert rule._errors.count() == 0


@patch("usdm3.rules.library.rule_template.RuleTemplate._ct_check")
def test_validate(mock_ct_check, rule):
    """Test validate method with ct_check"""
    rule.validate({"data": {}, "ct": {}})
    mock_ct_check.side_effect = [True, True]
    mock_ct_check.assert_has_calls([
        call({"data": {}, "ct": {}}, "StudyDesignPopulation", "plannedSex"),
        call({"data": {}, "ct": {}}, "StudyCohort", "plannedSex"),
    ])
