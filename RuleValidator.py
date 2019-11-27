import yaml
import json


class RuleViolation:
    def __init__(self, identifier, message='', path=None):
        self.path = path
        self.identifier = identifier
        self.message = message

    def __eq__(self, other):
        return self.identifier == other.identifier


class InvalidFormatException(Exception):
    pass


class RuleValidator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.rules = []

    def validate(self):
        violations = []

        ext = self.file_path.split('.')[::-1][0]

        if ext not in ['yml', 'yaml', 'json']:
            raise InvalidFormatException()

        with open(self.file_path) as file:
            spec = self.load_spec_file(file, ext)

            for rule in self.rules:
                rule_violations = rule.validate(spec)

                for rule_violation in rule_violations:
                    violations.append(rule_violation)
        return violations

    def add_rule(self, rule):
        self.rules.append(rule)

    def load_spec_file(self, file, ext):
        if ext in ['yml', 'yaml']:
            return yaml.load(file, Loader=yaml.FullLoader)
        elif ext == 'json':
            return json.load(file)
