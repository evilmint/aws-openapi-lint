from RuleValidator import RuleViolation


class AuthorizerOnOptionsRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in spec['paths'][path]:
                if path_verb.lower() != 'options':
                    continue

                has_security = 'security' in spec['paths'][path][path_verb]

                if has_security:
                    violations.append(RuleViolation('authorizer_on_options',
                                                    message='Unexpected authorizer on OPTIONS.',
                                                    path=path))

        return violations
