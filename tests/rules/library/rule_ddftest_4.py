from usdm3.rules.library.rule_template import RuleTemplate


class TestRule4(RuleTemplate):
    def __init__(self):
        super().__init__(
            "TEST_RULE_4",
            RuleTemplate.ERROR,
            "The test rule is blah blah blah",
        )

    def validate(self, config: dict) -> bool:
        raise Exception("This is a test exception")
