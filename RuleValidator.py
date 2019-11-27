import yaml


class RuleViolation:
    def __init__(self, identifier, message='', path=None):
        self.path = path
        self.identifier = identifier
        self.message = message

    def __eq__(self, other):
        return self.identifier == other.identifier


class RuleValidator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.rules = []

    def validate(self):
        violations = []

        with open(self.file_path) as file:
            spec = yaml.load(file, Loader=yaml.FullLoader)

            for rule in self.rules:
                rule_violations = rule.validate(spec)

                for rule_violation in rule_violations:
                    violations.append(rule_violation)
        return violations

    def add_rule(self, rule):
        self.rules.append(rule)
