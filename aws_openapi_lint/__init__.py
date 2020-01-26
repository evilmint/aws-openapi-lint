#!/usr/bin/env python3
# coding=utf-8

from .bcolors import bcolors
from .rules.CORSInconsistentHeadersRule import CORSInconsistentHeadersRule
from .rules.CORSNotEnoughVerbsRule import CORSNotEnoughVerbsRule
from .rules.ConflictingHttpVerbsRule import ConflictingHttpVerbsRule
from .rules.IntegrationBaseUriRule import IntegrationBaseUriRule
from .rules.MissingAmazonIntegrationRule import MissingAmazonIntegrationRule
from .rules.NoCORSPresentRule import NoCORSPresentRule
from .rules.PathParamNotMappedRule import PathParamNotMappedRule
from .rules.AuthorizerOnOptionsRule import AuthorizerOnOptionsRule
from .rules.AuthorizerReferencedButMissingRule import AuthorizerReferencedButMissingRule
from .rules.rule_validator import RuleValidator
import sys
import argparse


def print_violations(violations):
    for violation in violations:
        print(violation.identifier, violation.message, violation.path)

    violation_string = "violations"
    if len(violations) == 1:
        violation_string = "violation"

    print(bcolors.FAIL + "{} {} found.".format(len(violations), violation_string))


def print_no_violations():
    print(bcolors.OKGREEN + "0 violations found. Well done 💚")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Lint OpenAPI specifications based on AWS API Gateway.')
    parser.add_argument('lint_file', help='Specify path to the openapi schema file.')
    parser.add_argument('--treat-errors-as-warnings', action='store_const', const=True, default=False,
                        help='Treats errors as warnings (exit code will be 0 unless warning threshold is specified')
    parser.add_argument('--warning-threshold', default=-1, type=int, help='Warning threshold which when surpassed '
                                                                          'renders exit code to become 1)')
    parser.add_argument('--exclude-rules', default="", type=str, help='Excluded rules separated by comma.')
    parser.add_argument('--check-base-uri', default="", type=str, help='Checks whether every integration\'s '
                                                                       'path is equal to the base uri specified.')
    return parser.parse_args()


def cli(args=None, input_format="yaml", program_name="aws-openapi-lint"):
    if len(sys.argv) == 1:
        print('File path not passed as command line argument.')
        exit(1)

    args = parse_arguments()

    supported_rules = [
        ConflictingHttpVerbsRule(),
        MissingAmazonIntegrationRule(),
        PathParamNotMappedRule(),
        AuthorizerOnOptionsRule(),
        AuthorizerReferencedButMissingRule(),
        NoCORSPresentRule(),
        CORSNotEnoughVerbsRule(),
        CORSInconsistentHeadersRule()
    ]

    exclude_rules = args.exclude_rules.split(",")
    effective_rules = filter(lambda r: r.rule_name not in exclude_rules, supported_rules)

    rule_validator = RuleValidator(args.lint_file)

    for rule in effective_rules:
        rule_validator.add_rule(rule)

    if args.check_base_uri != "":
        rule_validator.add_rule(IntegrationBaseUriRule(base_uri=args.check_base_uri))

    violations = rule_validator.validate()

    if len(violations) == 0:
        print_no_violations()
    else:
        print_violations(violations)

    if args.treat_errors_as_warnings:
        if args.warning_threshold != -1 and len(violations) > args.warning_threshold:
            print("Warning threshold exceeded: {}/{}".format(len(violations), args.warning_threshold))
            exit(1)
        else:
            exit(0)
    else:
        exit(0 if len(violations) == 0 else 1)
