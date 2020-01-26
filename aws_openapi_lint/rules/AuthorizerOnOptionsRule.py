from .rule_validator import RuleViolation
from .rules_helper import get_path_verbs, has_security_components


class AuthorizerOnOptionsRule:
    def __init__(self):
        self.rule_name = 'authorizer_on_options'

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in get_path_verbs(spec, path):
                if path_verb != 'options':
                    continue

                if has_security_components(spec, path, path_verb):
                    violations.append(RuleViolation('authorizer_on_options',
                                                    message='Unexpected authorizer on OPTIONS.',
                                                    path=path))

        return violations
