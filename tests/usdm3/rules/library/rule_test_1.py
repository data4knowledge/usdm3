from usdm3.rules.library.rule_template import RuleTemplate


class TestRule1(RuleTemplate):
    def __init__(self):
        super().__init__(
            "TEST_RULE_1",
            RuleTemplate.ERROR,
            "blah blah blah",
        )

    def validate(self, config: dict) -> bool:
        return True
