from .rule_validator import RuleViolation
from .rules_helper import get_apigateway_integration, get_path_headers, get_integration_response_parameters, \
    get_path_verbs


class CORSInconsistentHeadersRule:
    def __init__(self):
        self.rule_name = 'options_cors_incosistent_headers'

    def validate(self, spec):
        violations = []

        for path in spec['paths']:
            if 'options' not in get_path_verbs(spec, path):
                continue

            integration = get_apigateway_integration(spec, path, 'options')
            path_headers = get_path_headers(spec, path)

            for response in integration['responses']:
                if 'responses' not in integration or response not in integration['responses'] or \
                        'responseParameters' not in integration['responses'][response]:
                    continue

                integration_response_params = get_integration_response_parameters(spec, path, 'options', response)

                if 'method.response.header.Access-Control-Allow-Headers' in integration_response_params:
                    integration_headers = self.get_access_control_allow_headers(integration_response_params)
                    headers_difference = set(path_headers).symmetric_difference(set(integration_headers))

                    for header in headers_difference:
                        message = 'Extra Allow-Header "{}" included in parameters or responseParameters.'.format(header)
                        violations.append(RuleViolation('options_cors_incosistent_headers',
                                                        message=message,
                                                        path=path))

        return violations

    def get_access_control_allow_headers(self, integration_response_params):
        allow_headers_value = integration_response_params['method.response.header.Access-Control-Allow-Headers']

        split_headers = map(lambda x: x.strip(), allow_headers_value[1:-1].split(','))
        split_headers = filter(lambda h: len(h.strip()) > 0, split_headers)

        return split_headers
