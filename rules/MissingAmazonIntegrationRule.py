from rule_validator import RuleViolation
from rules.rules_helper import contains_apigateway_integration


class MissingAmazonIntegrationRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in spec['paths'][path]:
                path_object = spec['paths'][path][path_verb]

                if not contains_apigateway_integration(path_object):
                    violations.append(RuleViolation('missing_amazon_integration',
                                                    message='Missing API Gateway integration',
                                                    path=path))

        return violations
