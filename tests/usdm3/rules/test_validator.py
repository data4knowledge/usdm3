from usdm3.rules.rules_validation import RulesValidation


def test_load_rules():
    """Test loading rules"""
    validator = RulesValidation("mixed_library")
    validator._load_rules()
    assert len(validator.rules) == 3


def test_execute_rules_valid():
    """Test executing rules with passing rule"""
    validator = RulesValidation("valid_library")
    validator._load_rules()
    results = validator._execute_rules({"data": {}, "ct": {}})
    assert results.count() == 1
    assert results.passed()


def test_execute_rules_invalid():
    """Test executing rules with failing rule"""
    validator = RulesValidation("invalid_library")
    validator._load_rules()
    results = validator._execute_rules({"data": {}, "ct": {}})
    assert results.count() == 1
    assert results.to_dict()["TEST_RULE_2"] == {
        "status": "Failure",
        "errors": [
            {
                "level": "Error",
                "message": "Unique message",
                "location": {
                    "rule": "TEST_RULE_2",
                    "rule_text": "The test rule is blah blah blah",
                    "klass": "klass",
                    "attribute": "attribute",
                    "path": "id",
                },
            }
        ],
        "exception": None,
    }


def test_execute_rules_not_implemented():
    """Test executing rules with rule that has not implemented validate"""
    validator = RulesValidation("not_implemented_library")
    validator._load_rules()
    results = validator._execute_rules({"data": {}, "ct": {}})
    assert results.count() == 1
    assert results.to_dict()["TEST_RULE_3"] == {
        "status": "Not Implemented",
        "errors": None,
        "exception": None,
    }


def test_execute_rules_exception():
    """Test executing rules with rule that raises an exception"""
    validator = RulesValidation("exception_library")
    validator._load_rules()
    results = validator._execute_rules({"data": {}, "ct": {}})
    assert results.count() == 1
    assert results.to_dict()["TEST_RULE_4"] == {
        "status": "Exception",
        "errors": None,
        "exception": "This is a test exception",
    }
