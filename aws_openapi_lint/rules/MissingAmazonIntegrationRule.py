from .rule_validator import RuleViolation
from .rules_helper import contains_apigateway_integration, get_path_verbs


class MissingAmazonIntegrationRule:
    def __init__(self):
        self.rule_name = 'missing_amazon_integration'

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in get_path_verbs(spec, path):
                path_object = spec['paths'][path][path_verb]

                if not contains_apigateway_integration(path_object):
                    violations.append(RuleViolation('missing_amazon_integration',
                                                    message='Missing API Gateway integration',
                                                    path=path))

        return violations
