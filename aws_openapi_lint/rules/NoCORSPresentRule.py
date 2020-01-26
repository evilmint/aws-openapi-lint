from .rule_validator import RuleViolation
from .rules_helper import path_contains_verb, get_apigateway_integration, get_integration_response_parameters


class NoCORSPresentRule:
    def __init__(self):
        self.rule_name = 'options_no_cors_present'

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

                if not self.response_params_contain_access_control_headers(response_params):
                    violations.append(RuleViolation('options_no_cors_present',
                                                    message='No CORS present.',
                                                    path=path))

        return violations

    def response_params_contain_access_control_headers(self, response_params):
        return 'method.response.header.Access-Control-Allow-Origin' in response_params and \
               'method.response.header.Access-Control-Allow-Methods' in response_params and \
               'method.response.header.Access-Control-Allow-Headers' in response_params

    def no_options_present_rule_violation(self, path):
        return RuleViolation('options_no_cors_present',
                             message='No OPTIONS',
                             path=path)
