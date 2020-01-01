from rule_validator import RuleViolation
from rules.rules_helper import get_apigateway_integration, get_path_headers, get_integration_response_parameters


class CORSInconsistentHeadersRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []

        for path in spec['paths']:
            if 'options' not in spec['paths'][path]:
                continue

            integration = get_apigateway_integration(spec, path, 'options')
            headers = get_path_headers(spec, path)

            for response in integration['responses']:
                if 'responses' not in integration or response not in integration['responses'] or \
                        'responseParameters' not in integration['responses'][response]:
                    continue

                response_params = get_integration_response_parameters(spec, path, 'options', response)

                if 'method.response.header.Access-Control-Allow-Headers' not in response_params:
                    violations.append(RuleViolation('options_cors_incosistent_headers',
                                                    message='No OPTIONS',
                                                    path=path))
                else:
                    methods = response_params['method.response.header.Access-Control-Allow-Headers']

                    split_headers = map(lambda x: x.strip(), methods[1:-1].split(','))
                    split_headers = filter(lambda h: len(h.strip()) > 0, split_headers)

                    symmetric_difference = set(headers).symmetric_difference(set(split_headers))

                    for unsupported_header in symmetric_difference:
                        message = 'Extra Allow-Header "{}" included in parameters or responseParameters.'\
                            .format(unsupported_header)
                        violations.append(RuleViolation('options_cors_incosistent_headers',
                                                        message=message,
                                                        path=path))

        return violations
