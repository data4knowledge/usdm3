import pytest
from unittest.mock import patch, call
from usdm3.rules.library.rule_ddf00146 import RuleDDF00146
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00146()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00146"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A study title type must be specified using the study title type (C207419) DDF codelist."
    )
    assert rule._errors.count() == 0


@patch("usdm3.rules.library.rule_template.RuleTemplate._ct_check")
def test_validate(mock_ct_check, rule):
    """Test validate method with ct_check"""
    rule.validate({"data": {}, "ct": {}})
    mock_ct_check.side_effect = [True]
    mock_ct_check.assert_has_calls(
        [
            call({"data": {}, "ct": {}}, "StudyTitle", "type"),
        ]
    )
