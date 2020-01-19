# OpenAPI AWS API Gateway linter

[![codecov](https://codecov.io/gh/evilmint/aws-openapi-lint/branch/master/graph/badge.svg)](https://codecov.io/gh/evilmint/aws-openapi-lint) [![license](https://img.shields.io/github/license/evilmint/aws-openapi-lint)](https://github.com/evilmint/aws-openapi-lint)

AWS-OpenAPI-Lint is a simple OpenAPI 3 yaml / json spec linter designed for checking API Gateway integration.

## Rules

It contains rules for checking whether:

- you have an authorizer on OPTIONS
- authorizer is mentioned in `requestParameters` but is not present in `security`
- http verbs are consistent in the path and integration
- all used headers in path from all verbs are mentioned in CORS rules and vice-versa
- CORS rules allow all verbs mentioned in the path
- CORS rules are present
- amazon integration is present
- path parameters present in `requestParameters` are not used in the direct path parameters and vice-versa

## Roadmap

- [X] Support json specs
- [ ] Ignore path-params if `http_proxy` integration type used
- [ ] Add option to disable rules via CLI
- [ ] Add option to disable rules for specific paths
- [X] Add warning threshold to return with status code 0 if limit not exceeded
- [X] Fix flake8 violations
- [X] Add a license
- [X] Publish to PyPI or alike
- [X] Configure properly up GitHub actions to run tests on push

## Installation

```
pip install aws-openapi-lint
```

## Usage

`$ aws-openapi-lint path/to/spec.yml`

```
usage: aws-openapi-lint [-h] [--treat-errors-as-warnings]
                        [--warning-threshold WARNING_THRESHOLD]
                        lint_file

Lint OpenAPI specifications based on AWS API Gateway.

positional arguments:
  lint_file             Specify path to the openapi schema file.

optional arguments:
  -h, --help            show this help message and exit
  --treat-errors-as-warnings
                        Treats errors as warnings (exit code will be 0 unless
                        warning threshold is specified
  --warning-threshold WARNING_THRESHOLD
                        Warning threshold which when surpassed renders exit
                        code to become 1)

```

The program terminates with exit code equal to the amount of violations found.
