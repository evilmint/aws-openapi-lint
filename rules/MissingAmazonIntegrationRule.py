from RuleValidator import RuleViolation


class MissingAmazonIntegrationRule:
    def __init__(self):
        pass

    def validate(self, spec):
        violations = []
        for path in spec['paths']:
            for path_verb in spec['paths'][path]:
                verb_map = spec['paths'][path][path_verb]

                if 'x-amazon-apigateway-integration' not in verb_map:
                    violations.append(RuleViolation('missing_amazon_integration',
                                                    message='Missing API Gateway integration',
                                                    path=path))

        return violations
