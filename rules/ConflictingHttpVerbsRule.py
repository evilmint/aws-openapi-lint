from rule_validator import RuleViolation


class ConflictingHttpVerbsRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in spec['paths'][path]:
                if path_verb.lower() == 'options':
                    continue

                if 'httpMethod' not in spec['paths'][path][path_verb]['x-amazon-apigateway-integration']:
                    continue

                integration_verb = spec['paths'][path][path_verb]['x-amazon-apigateway-integration']['httpMethod']

                if path_verb.lower() != integration_verb.lower():
                    message = 'Path verb "%s" is not equal to integration httpMethod verb "%s".' \
                              % (path_verb.upper(), integration_verb)
                    violations.append(RuleViolation('conflicting_http_verbs', message, path))
        return violations
