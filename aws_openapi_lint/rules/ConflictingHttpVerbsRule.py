from .rule_validator import RuleViolation
from .rules_helper import contains_apigateway_integration, get_integration_verb, get_path_verbs


class ConflictingHttpVerbsRule:
    def __init__(self):
        self.rule_name = 'conflicting_http_verbs'

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in get_path_verbs(spec, path):
                if path_verb == 'options':
                    continue

                if not contains_apigateway_integration(spec['paths'][path][path_verb]):
                    continue

                integration_verb = get_integration_verb(spec, path, path_verb)

                if path_verb.lower() != integration_verb.lower():
                    message = 'Path verb "%s" is not equal to integration httpMethod verb "%s".' \
                              % (path_verb.upper(), integration_verb)
                    violations.append(RuleViolation('conflicting_http_verbs', message, path))
        return violations
