import unittest

from aws_openapi_lint import IntegrationBaseUriRule
from aws_openapi_lint.rules.AuthorizerOnOptionsRule import AuthorizerOnOptionsRule
from aws_openapi_lint.rules.AuthorizerReferencedButMissingRule import AuthorizerReferencedButMissingRule
from aws_openapi_lint.rules.CORSInconsistentHeadersRule import CORSInconsistentHeadersRule
from aws_openapi_lint.rules.CORSNotEnoughVerbsRule import CORSNotEnoughVerbsRule
from aws_openapi_lint.rules.ConflictingHttpVerbsRule import ConflictingHttpVerbsRule
from aws_openapi_lint.rules.MissingAmazonIntegrationRule import MissingAmazonIntegrationRule
from aws_openapi_lint.rules.NoCORSPresentRule import NoCORSPresentRule
from aws_openapi_lint.rules.PathParamNotMappedRule import PathParamNotMappedRule
from aws_openapi_lint.rules.rule_validator import RuleValidator, RuleViolation


class RuleValidatorTestCase(unittest.TestCase):
    def test_should_return_conflicting_verbs_rule_violation(self):
        rule_validator = RuleValidator(spec_path('conflicting_http_verbs_spec'))
        rule_validator.add_rule(ConflictingHttpVerbsRule())
        self.assertEqual([RuleViolation('conflicting_http_verbs')], rule_validator.validate())

    def test_should_return_missing_amazon_integration_rule_violation(self):
        rule_validator = RuleValidator(spec_path('no_amazon_integration'))
        rule_validator.add_rule(MissingAmazonIntegrationRule())
        self.assertEqual([RuleViolation('missing_amazon_integration')], rule_validator.validate())

    def test_should_return_no_cors_present_rule_violation(self):
        rule_validator = RuleValidator(spec_path('options_no_cors_present'))
        rule_validator.add_rule(NoCORSPresentRule())
        self.assertEqual([RuleViolation('options_no_cors_present')], rule_validator.validate())

    def test_should_return_cors_not_enough_verbs_rule_violation(self):
        rule_validator = RuleValidator(spec_path('options_cors_inconsistent_verbs'))
        rule_validator.add_rule(CORSNotEnoughVerbsRule())
        self.assertEqual([RuleViolation('options_cors_not_enough_verbs')], rule_validator.validate())

    def test_should_return_cors_inconsistent_headers_rule_violation(self):
        rule_validator = RuleValidator(spec_path('options_cors_incosistent_headers'))
        rule_validator.add_rule(CORSInconsistentHeadersRule())
        self.assertEqual([RuleViolation('options_cors_incosistent_headers')], rule_validator.validate())

    def test_should_return_authorizer_absent_but_referenced_in_request_params_rule_violation(self):
        rule_validator = RuleValidator(spec_path('authorizer_referenced_but_missing'))
        rule_validator.add_rule(AuthorizerReferencedButMissingRule())
        self.assertEqual([RuleViolation('authorizer_referenced_but_missing')], rule_validator.validate())

    def test_should_return_no_authorizer_on_options_rule_violation(self):
        rule_validator = RuleValidator(spec_path('no_authorizer_on_options'))
        rule_validator.add_rule(AuthorizerOnOptionsRule())
        self.assertEqual([RuleViolation('authorizer_on_options')], rule_validator.validate())

    def test_should_return_integration_base_uri_rule_violation(self):
        rule_validator = RuleValidator(spec_path('conflicting_base_uri'))
        rule_validator.add_rule(IntegrationBaseUriRule(base_uri='e'))
        self.assertEqual([RuleViolation('integration_base_uri')], rule_validator.validate())

    def test_ok_spec(self):
        rule_validator = RuleValidator(spec_path('ok_spec'))
        rule_validator.add_rule(ConflictingHttpVerbsRule())
        self.assertEqual([], rule_validator.validate())

    def test_ok_spec_json(self):
        rule_validator = RuleValidator('test_files/ok_spec_json.json')
        rule_validator.add_rule(ConflictingHttpVerbsRule())
        self.assertEqual([], rule_validator.validate())

    def test_should_not_return_violations_if_path_param_not_mapped_and_mock_integration(self):
        rule_validator = RuleValidator(spec_path('path_parameter_not_mapped_mock'))
        rule_validator.add_rule(PathParamNotMappedRule())
        self.assertEqual([], rule_validator.validate())

    def test_should_return_path_param_not_mapped_rule_violation(self):
        rule_validator = RuleValidator(spec_path('path_parameter_not_mapped'))
        rule_validator.add_rule(PathParamNotMappedRule())
        self.assertEqual([RuleViolation('path_parameter_not_mapped'), RuleViolation('path_parameter_not_mapped')],
                         rule_validator.validate())


def spec_path(file_name):
    return './test_files/' + file_name + '.yml'


if __name__ == '__main__':
    unittest.main()
