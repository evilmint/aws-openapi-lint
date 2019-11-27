#!/usr/bin/python
# coding=utf-8

from bcolors import bcolors
from rules.CORSInconsistentHeadersRule import CORSInconsistentHeadersRule
from rules.CORSNotEnoughVerbsRule import CORSNotEnoughVerbsRule
from rules.ConflictingHttpVerbsRule import ConflictingHttpVerbsRule
from rules.MissingAmazonIntegrationRule import MissingAmazonIntegrationRule
from rules.NoCORSPresentRule import NoCORSPresentRule
from rules.PathParamNotMappedRule import PathParamNotMappedRule
from rules.AuthorizerOnOptionsRule import AuthorizerOnOptionsRule
from rules.AuthorizerReferencedButMissingRule import AuthorizerReferencedButMissingRule
from RuleValidator import *
import sys


def print_violations(violations):
    for violation in violations:
        print(violation.identifier, violation.message, violation.path)

    violation_string = "violations"
    if len(violations) == 1:
        violation_string = "violation"

    print(bcolors.FAIL + "{} {} found.".format(len(violations), violation_string))


def print_no_violations():
    print(bcolors.OKGREEN + "0 violations found. Well done 💚")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('File path not passed as command line argument.')
        exit(1)

    rule_validator = RuleValidator(sys.argv[1])
    rule_validator.add_rule(ConflictingHttpVerbsRule())
    rule_validator.add_rule(MissingAmazonIntegrationRule())
    rule_validator.add_rule(PathParamNotMappedRule())
    rule_validator.add_rule(AuthorizerOnOptionsRule())
    rule_validator.add_rule(AuthorizerReferencedButMissingRule())
    rule_validator.add_rule(NoCORSPresentRule())
    rule_validator.add_rule(CORSNotEnoughVerbsRule())
    rule_validator.add_rule(CORSInconsistentHeadersRule())

    violations = rule_validator.validate()

    if len(violations) == 0:
        print_no_violations()
    else:
        print_violations(violations)

    exit(len(violations))
