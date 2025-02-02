import os
import json
from jsonschema import validate, ValidationError, RefResolver


class SchemaValidator:
    def __init__(self, schema_file_path: str):
        """
        Initialize the validator with an OpenAPI schema file

        Args:
            schema_file_path (str): Path to the OpenAPI schema JSON file
        """
        self.schema_file_path = schema_file_path
        with open(schema_file_path, "r") as f:
            self.schema = json.load(f)

        # Create a resolver for handling $ref references in the schema
        schema_path = os.path.abspath(schema_file_path)
        schema_uri = f"file://{schema_path}"
        self.resolver = RefResolver(schema_uri, self.schema)

    def get_component_schema(self, component_name):
        """
        Get a specific component schema from the OpenAPI definitions

        Args:
            component_name (str): Name of the component schema (e.g., 'Wrapper-Input')

        Returns:
            dict: The component schema definition
        """
        if (
            "components" not in self.schema
            or "schemas" not in self.schema["components"]
        ):
            raise ValueError("Schema does not contain components/schemas section")

        if component_name not in self.schema["components"]["schemas"]:
            raise ValueError(f"Schema component '{component_name}' not found")

        return self.schema["components"]["schemas"][component_name]

    def validate_against_component(self, data, component_name):
        """
        Validate data against a specific component schema

        Args:
            data (dict): The JSON data to validate
            component_name (str): Name of the component schema to validate against

        Returns:
            bool: True if validation succeeds

        Raises:
            ValidationError: If validation fails
            ValueError: If component schema is not found
        """
        try:
            component_schema = self.get_component_schema(component_name)
            validate(instance=data, schema=component_schema, resolver=self.resolver)
            return True
        except ValidationError as e:
            print(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error during validation: {str(e)}")
            raise

    def validate_file(self, json_file_path, component_name):
        """
        Validate a JSON file against a component schema

        Args:
            json_file_path (str): Path to the JSON file to validate
            component_name (str): Name of the component schema to validate against

        Returns:
            bool: True if validation succeeds

        Raises:
            ValidationError: If validation fails
            ValueError: If component schema is not found
        """
        try:
            with open(json_file_path, "r") as f:
                data = json.load(f)
            return self.validate_against_component(data, component_name)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {str(e)}")
            raise
        except Exception as e:
            print(f"Error during file validation: {str(e)}")
            raise
