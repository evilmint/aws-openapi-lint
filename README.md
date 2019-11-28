[![codecov](https://codecov.io/gh/evilmint/aws-openapi-lint/branch/master/graph/badge.svg)](https://codecov.io/gh/evilmint/aws-openapi-lint) [![license](https://img.shields.io/github/license/evilmint/aws-openapi-lint)](https://github.com/evilmint/aws-openapi-lint)

# What does it do?

AWS-OpenAPI-Lint is a simple OpenAPI 3 yaml / json spec linter designed for checking API Gateway integration.

It contains rules for checking whether:

- you have an authorizer on OPTIONS
- authorizer is mentioned in `requestParameters` but is not present in `security`
- http verbs are consistent in the path and integration
- all used headers in path from all verbs are mentioned in CORS rules and vice-versa
- CORS rules allow all verbs mentioned in the path
- CORS rules are present
- amazon integration is present
- path parameters present in `requestParameters` are not used in the direct path parameters and vice-versa

# Roadmap

- [X] Support json specs
- [ ] Ignore path-params if `http_proxy` integration type used
- [ ] Add option to disable rules via CLI
- [ ] Add option to disable rules for specific paths
- [ ] Add warning threshold to return with status code 0 if limit not exceeded
- [ ] Fix flake8 violations
- [ ] Add a license
- [ ] Publish to PyPI or alike
- [X] Configure properly up GitHub actions to run tests on push

# Installation

```
git clone --recursive https://github.com/evilmint/aws-openapi-lint.git
cd aws-openapi-lint
python setup.py install
```

One of the options to use the script from the shell is to create a symlink to `main.py` by running

`sudo ln -s /path/to/main.py /usr/local/bin/aws-openapi-lint`

or simply add the script directory's path to `$PATH` by running

`PATH=$PATH:/path/to/mainpy/dir`

# Usage

Run `aws-openapi-lint path/to/spec.yml`

The program terminates with exit code equal to the amount of violations found.