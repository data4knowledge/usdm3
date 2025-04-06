import pathlib
from src.usdm3.rules.rules_validation import RulesValidationEngine


def library_path(path: str):
    return pathlib.Path(__file__).parent.parent.resolve()


def test_rules():
    """Test loading rules"""
    # RulesValidationEngine.__instance = None
    validator = RulesValidationEngine(library_path(""), "tests.rules.test_library")
    assert len(validator.rules) == 4
    results = validator._execute_rules({"data": {}, "ct": {}})
    assert results.count() == 4
    actual = results.to_dict()
    assert actual[3]["exception"].startswith("This is a test exception\n")
    actual[3]["exception"] = "This is a test exception" # has extra text from the traceback
    assert actual == [
        {
            "attribute": "",
            "exception": None,
            "klass": "",
            "level": "",
            "message": "",
            "path": "",
            "rule": "",
            "rule_id": "TEST_RULE_1",
            "rule_text": "",
            "status": "Success",
        },
        {
            "attribute": "attribute",
            "exception": None,
            "klass": "klass",
            "level": "Error",
            "message": "blah blah blah",
            "path": "id",
            "rule": "TEST_RULE_2",
            "rule_id": "TEST_RULE_2",
            "rule_text": "blah blah blah",
            "status": "Failure",
        },
        {
            "attribute": "",
            "exception": None,
            "klass": "",
            "level": "",
            "message": "",
            "path": "",
            "rule": "",
            "rule_id": "TEST_RULE_3",
            "rule_text": "",
            "status": "Not Implemented",
        },
        {
            "attribute": "",
            "exception": "This is a test exception",
            "klass": "",
            "level": "",
            "message": "",
            "path": "",
            "rule": "",
            "rule_id": "TEST_RULE_4",
            "rule_text": "",
            "status": "Exception",
        },
    ]
