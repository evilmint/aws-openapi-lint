from .rule_validator import RuleViolation
from .rules_helper import get_path_verbs, get_apigateway_integration


class IntegrationBaseUriRule:
    base_uri = ''

    def __init__(self, base_uri):
        self.rule_name = 'integration_base_uri'
        self.base_uri = base_uri

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in get_path_verbs(spec, path):
                if path_verb == 'options':
                    continue

                integration = get_apigateway_integration(spec, path, path_verb)
                integration_uri = integration['uri']

                if not integration_uri.startswith(self.base_uri):
                    violations.append(RuleViolation('integration_base_uri',
                                                    message='Base URI "{}" not present at the beginning of URI "{}"'
                                                    .format(self.base_uri, integration_uri),
                                                    path=path))

        return violations
