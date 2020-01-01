from rule_validator import RuleViolation
from rules.rules_helper import path_contains_verb, get_apigateway_integration, get_integration_response_parameters


class NoCORSPresentRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []

        for path in spec['paths']:
            if not path_contains_verb(spec, path, 'options'):
                continue

            integration = get_apigateway_integration(spec, path, 'options')

            for response in integration['responses']:
                if response not in integration['responses'] or \
                        'responseParameters' not in integration['responses'][response]:
                    violations.append(self.no_options_present_rule_violation(path))
                    continue

                response_params = get_integration_response_parameters(spec, path, 'options', response)

                if 'method.response.header.Access-Control-Allow-Origin' not in response_params or \
                        'method.response.header.Access-Control-Allow-Methods' not in response_params or \
                        'method.response.header.Access-Control-Allow-Headers' not in response_params:
                    violations.append(RuleViolation('options_no_cors_present',
                                                    message='No CORS present.',
                                                    path=path))

        return violations

    def no_options_present_rule_violation(self, path):
        return RuleViolation('options_no_cors_present',
                             message='No OPTIONS',
                             path=path)
