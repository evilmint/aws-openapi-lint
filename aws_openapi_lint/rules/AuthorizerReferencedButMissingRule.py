from .rule_validator import RuleViolation
from .rules_helper import contains_apigateway_integration, contains_request_parameters, \
    authorizer_referenced_in_request_params, has_security_components, get_path_verbs


class AuthorizerReferencedButMissingRule:
    def __init__(self):
        self.rule_name = 'authorizer_referenced_but_missing'

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in get_path_verbs(spec, path):
                if path_verb == 'options':
                    continue

                if not contains_apigateway_integration(spec['paths'][path][path_verb]) \
                        or not contains_request_parameters(spec['paths'][path][path_verb]):
                    continue

                if has_security_components(spec, path, path_verb):
                    return []

                if authorizer_referenced_in_request_params(spec, path, path_verb):
                    message = 'Authorizer referenced in `requestParameters` but absent in security.'
                    violations.append(RuleViolation('authorizer_referenced_but_missing',
                                                    message,
                                                    path=path))

        return violations
