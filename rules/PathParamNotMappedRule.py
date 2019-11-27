import re

from rule_validator import RuleViolation


class PathParamNotMappedRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []

        for path in spec['paths']:
            path_params = re.findall(r'(\{[a-zA-Z _\-0-9]+\})', path)
            path_params = map(lambda x: x.replace('{', '').replace('}', ''), path_params)

            for path_verb in spec['paths'][path]:
                if path_verb.lower() == 'options':
                    continue

                if 'x-amazon-apigateway-integration' not in spec['paths'][path][path_verb] \
                        or 'requestParameters' not in spec['paths'][path][path_verb]['x-amazon-apigateway-integration']:
                    continue

                integration = spec['paths'][path][path_verb]['x-amazon-apigateway-integration']

                if integration['type'].lower() == 'mock':
                    continue

                request_params = integration['requestParameters']

                for path_param in path_params:
                    if "integration.request.path.%s" % path_param not in request_params:
                        message = 'Path parameter "{}" was not mapped in `requestParameters`.'.format(path_param)
                        violations.append(RuleViolation('path_parameter_not_mapped',
                                                        message=message,
                                                        path=path))

        return violations
