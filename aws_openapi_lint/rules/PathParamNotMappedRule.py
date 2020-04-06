from functools import reduce

from .rule_validator import RuleViolation
from .rules_helper import find_path_params, contains_apigateway_integration, contains_request_parameters, \
    get_apigateway_integration, get_path_verbs


class PathParamNotMappedRule:
    def __init__(self):
        self.rule_name = 'path_parameter_not_mapped'

    def validate(self, spec):
        violations = []

        for path in spec['paths']:
            all_path_params = find_path_params(path)

            for path_verb in get_path_verbs(spec, path):
                if path_verb.lower() == 'options':
                    continue

                if not contains_apigateway_integration(spec['paths'][path][path_verb]) \
                        or not contains_request_parameters(spec['paths'][path][path_verb]):
                    continue

                integration = get_apigateway_integration(spec, path, path_verb)

                if integration['type'].lower() == 'mock':
                    continue

                request_params = integration['requestParameters']
                request_params_values = request_params.values()

                request_params_last = [value.split('.')[-1:] for value in request_params_values]
                request_params_last = reduce(lambda x, y: x+y, request_params_last)

                for path_param in all_path_params:
                    if path_param not in request_params_last:
                        message = 'Path parameter "{}" was not mapped in `requestParameters`.'.format(path_param)
                        violations.append(RuleViolation('path_parameter_not_mapped',
                                                        message=message,
                                                        path=path))

        return violations
