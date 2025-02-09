from usdm3.rules.rules_validation import Validator


def test_load_rules():
    """Test loading rules"""
    validator = Validator("library")
    validator.load_rules()
    assert len(validator.rules) == 3


def test_execute_rules_valid():
    """Test executing rules with passing rule"""
    validator = Validator("library")
    validator.load_rules()
    results = validator.execute_rules({"data": {}, "ct": {}})
    assert len(results) == 3
    assert results[0]["rule"] == "TestRule1"
    assert results[0]["valid"] is True
    assert results[0]["errors"].count() == 0
    assert results[0]["exception"] is None


def test_execute_rules_invalid():
    """Test executing rules with failing rule"""
    validator = Validator("library")
    validator.load_rules()
    results = validator.execute_rules({"data": {}, "ct": {}})
    assert len(results) == 3
    assert results[1]["rule"] == "TestRule2"
    assert results[1]["valid"] is False
    assert results[1]["errors"].count() == 1
    assert results[1]["exception"] is None


def test_execute_rules_not_implemented():
    """Test executing rules with rule that has not implemented validate"""
    validator = Validator("library")
    validator.load_rules()
    results = validator.execute_rules({"data": {}, "ct": {}})
    assert len(results) == 3
    assert results[2]["rule"] == "TestRule3"
    assert results[2]["valid"] is False
    assert results[2]["errors"] is None
    assert results[2]["exception"] == "not implemented"
