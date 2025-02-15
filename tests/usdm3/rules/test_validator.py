from usdm3.rules.rules_validation import RulesValidation
import pathlib
import os


def library_path(path: str):
    root = pathlib.Path(__file__).parent.resolve()
    path = os.path.join(root, path)
    print(f"path: {path}")
    return path


def test_rules():
    """Test loading rules"""
    validator = RulesValidation(
        library_path("test_library"), "tests.usdm3.rules.test_library"
    )
    assert len(validator.rules) == 4
    results = validator._execute_rules({"data": {}, "ct": {}})
    assert results.count() == 4
    assert results.to_dict() == [
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
