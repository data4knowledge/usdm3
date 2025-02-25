import pytest
from unittest.mock import patch
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


@patch("usdm3.rules.library.rule_template.RuleTemplate._ct_check")
def test_validate(mock_ct_check, rule):
    """Test validate method with ct_check"""
    rule.validate({"data": {}, "ct": {}})
    assert mock_ct_check.call_count == 1
    assert mock_ct_check.call_args[0][0] == {"data": {}, "ct": {}}
    assert mock_ct_check.call_args[0][1] == "StudyArm"
    assert mock_ct_check.call_args[0][2] == "dataOriginType"
