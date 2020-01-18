from .rule_validator import RuleViolation
from .rules_helper import find_path_params, contains_apigateway_integration, contains_request_parameters, \
    get_apigateway_integration, get_path_verbs


class PathParamNotMappedRule:
    def __init__(self):
        pass

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

                for path_param in all_path_params:
                    if "integration.request.path.%s" % path_param not in request_params:
                        message = 'Path parameter "{}" was not mapped in `requestParameters`.'.format(path_param)
                        violations.append(RuleViolation('path_parameter_not_mapped',
                                                        message=message,
                                                        path=path))

        return violations
