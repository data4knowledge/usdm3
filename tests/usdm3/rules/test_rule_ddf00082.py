import pytest
from unittest.mock import Mock, patch
from usdm3.rules.library.rule_ddf00082 import RuleDDF00082
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00082()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00082"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Data types of attributes (string, number, boolean) must conform with the USDM schema based on the API specification."
    )
    assert rule._errors.count() == 0


@patch("usdm3.rules.library.schema.schema_validation.SchemaValidation.validate_file")
def test_validate_passed(mock_validate_file, rule):
    data_store = Mock()
    data_store.filename = "filename.txt"

    mock_validate_file.return_value = True
    result = rule.validate({"data": data_store})
    assert result 


def test_validate_fails(rule):
    data_store = Mock()
    data_store.filename = "filename.txt"

    with patch(
        "usdm3.rules.library.schema.schema_validation.SchemaValidation.validate_file",
        side_effect=Exception("ValidationError"),
    ):
        with pytest.raises(Exception): # as excinfo: ... removed from ruff check but keep as a reminder
            result = rule.validate({"data": data_store})
            assert not result
