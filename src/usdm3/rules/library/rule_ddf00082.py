from .rule_template import RuleTemplate
from usdm3.schema.schema_location import SchemaErrorLocation
from usdm3.schema.schema_validation import SchemaValidation, ValidationError
from usdm3.data_store.data_store import DataStore


class RuleDDF00082(RuleTemplate):
    """
    DDF00082: Data types of attributes (string, number, boolean) must conform with the USDM schema based on the API specification.

    Applies to: All
    Attributes: All
    """

    def __init__(self):
        super().__init__(
            "DDF00082",
            RuleTemplate.ERROR,
            "Data types of attributes (string, number, boolean) must conform with the USDM schema based on the API specification.",
        )

    def validate(self, config: dict) -> bool:

        try:
            data: DataStore = config["data"]
            schema_path = "schema/usdm_v3.json"
            validator = SchemaValidation(schema_path)
            validator.validate_file(data.filename, "Wrapper-Input")
            return True
        except ValidationError as e:
            location = SchemaErrorLocation(e.json_path, e.instance)
            self._errors.add(e.message, location)
            return False
