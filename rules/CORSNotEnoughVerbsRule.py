import re

from RuleValidator import RuleViolation
from sets import Set

class CORSNotEnoughVerbsRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []

        for path in spec['paths']:
            if 'options' not in spec['paths'][path]:
                violations.append(RuleViolation('options_cors_not_enough_verbs',
                                                message='No OPTIONS',
                                                path=path))
                continue

            integration = spec['paths'][path]['options']['x-amazon-apigateway-integration']

            verbs = spec['paths'][path].keys()
            verbs = map(lambda x: x.lower(), verbs)

            for response in integration['responses']:
                if 'responses' not in integration or response not in integration['responses'] or \
                        'responseParameters' not in integration['responses'][response]:
                    violations.append(RuleViolation('options_cors_not_enough_verbs',
                                                    message='No OPTIONS',
                                                    path=path))
                    continue

                response_params = integration['responses'][response]['responseParameters']

                if 'method.response.header.Access-Control-Allow-Methods' not in response_params:
                    violations.append(RuleViolation('options_cors_not_enough_verbs',
                                                    message='No OPTIONS',
                                                    path=path))
                else:
                    methods = response_params['method.response.header.Access-Control-Allow-Methods']

                    split_methods = map(lambda x: x.lower().strip(), methods[1:-1].split(','))

                    symmetric_difference = Set(verbs).symmetric_difference(Set(split_methods))

                    for unsupported_verb in symmetric_difference:
                        message = 'Extra HTTP verb {} included in path or request mapping.'.format(unsupported_verb)
                        violations.append(RuleViolation('options_cors_not_enough_verbs',
                                                        message=message,
                                                        path=path))

        return violations
