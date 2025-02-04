from usdm3.rules.library.rule_template import RuleTemplate


class TestRule3(RuleTemplate):
    def __init__(self):
        super().__init__("TEST_RULE_3", RuleTemplate.ERROR, "blah blah blah")

