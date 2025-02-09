from usdm3.rules.library.rule_template import RuleTemplate, JSONLocation


class TestRule2(RuleTemplate):
    def __init__(self):
        super().__init__(
            "TEST_RULE_2",
            RuleTemplate.ERROR,
            "blah blah blah",
        )

    def validate(self, config: dict) -> bool:
        self._add_failure(
            "blah blah blah",
            "klass",
            "attribute",
            "id",
        )
        return False
