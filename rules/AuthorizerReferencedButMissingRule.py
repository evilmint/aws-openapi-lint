from rule_validator import RuleViolation


class AuthorizerReferencedButMissingRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in spec['paths'][path]:
                if path_verb.lower() == 'options':
                    continue

                if 'x-amazon-apigateway-integration' not in spec['paths'][path][path_verb] \
                        or 'requestParameters' not in spec['paths'][path][path_verb]['x-amazon-apigateway-integration']:
                    continue

                integration = spec['paths'][path][path_verb]['x-amazon-apigateway-integration']

                has_security = 'security' in spec['paths'][path][path_verb]

                if has_security and len(spec['paths'][path][path_verb]['security']) > 0:
                    return []

                request_params = integration['requestParameters']

                for request_param in request_params.values():
                    if request_param.startswith('context.authorizer'):
                        message = 'Authorizer referenced in `requestParameters` but absent in security.'
                        violations.append(RuleViolation('authorizer_referenced_but_missing',
                                                        message,
                                                        path=path))

        return violations
