from .rule_validator import RuleViolation
from .rules_helper import get_path_verbs, get_apigateway_integration, path_contains_verb, \
    get_integration_response_parameters


class CORSNotEnoughVerbsRule:
    def __init__(self):
        self.rule_name = 'options_cors_not_enough_verbs'

    def validate(self, spec):
        violations = []

        for path in spec['paths']:
            if not path_contains_verb(spec, path, 'options'):
                violations.append(self.missing_options_verb_rule_violation(path))
                continue

            integration = get_apigateway_integration(spec, path, 'options')
            path_verbs = get_path_verbs(spec, path)

            for response in integration['responses']:
                if 'responses' not in integration or response not in integration['responses'] or \
                        'responseParameters' not in integration['responses'][response]:
                    violations.append(self.missing_options_verb_rule_violation(path))
                    continue

                response_params = get_integration_response_parameters(spec, path, 'options', response)

                if 'method.response.header.Access-Control-Allow-Methods' not in response_params:
                    violations.append(self.missing_options_verb_rule_violation(path))
                else:
                    allow_methods_value = response_params['method.response.header.Access-Control-Allow-Methods']
                    integration_verbs = map(lambda x: x.lower().strip(), allow_methods_value[1:-1].split(','))

                    verbs_difference = set(path_verbs).symmetric_difference(set(integration_verbs))

                    for verb in verbs_difference:
                        message = 'Extra HTTP verb {} included in path or request mapping.'.format(verb)
                        violations.append(RuleViolation('options_cors_not_enough_verbs',
                                                        message=message,
                                                        path=path))

        return violations

    def missing_options_verb_rule_violation(self, path):
        return RuleViolation('options_cors_not_enough_verbs',
                             message='Missing OPTIONS verb',
                             path=path)
