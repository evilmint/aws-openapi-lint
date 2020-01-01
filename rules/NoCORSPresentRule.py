from rule_validator import RuleViolation


class NoCORSPresentRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []

        for path in spec['paths']:
            if 'options' not in spec['paths'][path]:
                continue
            path_verb = 'options'

            integration = spec['paths'][path][path_verb]['x-amazon-apigateway-integration']

            for response in integration['responses']:
                if 'responses' not in integration or response not in integration['responses'] or \
                        'responseParameters' not in integration['responses'][response]:
                    violations.append(RuleViolation('options_no_cors_present',
                                                    message='No OPTIONS',
                                                    path=path))
                    continue

                response_params = integration['responses'][response]['responseParameters']

                if 'method.response.header.Access-Control-Allow-Origin' not in response_params or \
                        'method.response.header.Access-Control-Allow-Methods' not in response_params or \
                        'method.response.header.Access-Control-Allow-Headers' not in response_params:
                    violations.append(RuleViolation('options_no_cors_present',
                                                    message='No CORS present.',
                                                    path=path))

        return violations
