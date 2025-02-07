import pytest
import json
from pathlib import Path
from unittest.mock import mock_open, patch
from usdm3.schema.schema_validation import SchemaValidator

# Sample schema for testing
MOCK_SCHEMA = {
    "components": {
        "schemas": {
            "Test-Component": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
                "required": ["name"],
            }
        }
    }
}


@pytest.fixture
def schema_validator():
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_SCHEMA))):
        return SchemaValidator("dummy/path.json")


def test_init_schema_validator():
    """Test SchemaValidator initialization"""
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_SCHEMA))):
        validator = SchemaValidator("dummy/path.json")
        assert validator.schema == MOCK_SCHEMA


def test_get_component_schema(schema_validator):
    """Test getting component schema"""
    component = schema_validator.get_component_schema("Test-Component")
    assert component == MOCK_SCHEMA["components"]["schemas"]["Test-Component"]


def test_get_component_schema_invalid(schema_validator):
    """Test getting non-existent component schema"""
    with pytest.raises(
        ValueError, match="Schema component 'Invalid-Component' not found"
    ):
        schema_validator.get_component_schema("Invalid-Component")


def test_validate_against_component_valid(schema_validator):
    """Test successful validation against component"""
    valid_data = {"name": "John", "age": 30}
    assert (
        schema_validator.validate_against_component(valid_data, "Test-Component")
        is True
    )


def test_validate_against_component_invalid(schema_validator):
    """Test failed validation against component"""
    invalid_data = {"age": 30}  # Missing required 'name' field
    with pytest.raises(SchemaValidator.SchemaValidatorError, match="validation error"):
        schema_validator.validate_against_component(invalid_data, "Test-Component")


def test_validate_file(schema_validator):
    """Test validating JSON file"""
    valid_data = {"name": "John", "age": 30}
    mock_file = mock_open(read_data=json.dumps(valid_data))

    with patch("builtins.open", mock_file):
        assert (
            schema_validator.validate_file("dummy/data.json", "Test-Component") is True
        )


def test_validate_file_invalid_json(schema_validator):
    """Test validating invalid JSON file"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with pytest.raises(
            SchemaValidator.SchemaValidatorError, match="error reading JSON file"
        ):
            schema_validator.validate_file("dummy/invalid.json", "Test-Component")


def test_validate_file_validation_error(schema_validator):
    """Test validating file with invalid data"""
    invalid_data = {"age": 30}  # Missing required 'name' field
    mock_file = mock_open(read_data=json.dumps(invalid_data))

    with patch("builtins.open", mock_file):
        with pytest.raises(
            SchemaValidator.SchemaValidatorError, match="validation error"
        ):
            schema_validator.validate_file("dummy/data.json", "Test-Component")


def test_schema_without_components():
    """Test initialization with schema missing components section"""
    invalid_schema = {}
    with patch("builtins.open", mock_open(read_data=json.dumps(invalid_schema))):
        validator = SchemaValidator("dummy/path.json")
        with pytest.raises(
            ValueError, match="Schema does not contain components/schemas section"
        ):
            validator.get_component_schema("Test-Component")
