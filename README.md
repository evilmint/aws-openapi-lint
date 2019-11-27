# What does it do?

AWS-OpenAPI-Lint is a simple linter to check OpenAPI 3 yaml specs for inconsistencies and violations.

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

- [ ] Ignore path-params if `http_proxy` integration type used
- [ ] Support json specs
- [ ] Add option to disable rules via CLI
- [ ] Add option to disable rules for specific paths
- [ ] Add warning threshold to not return with status code other than 0 if limit not exceeded

# Installation

One of the options to use the script from the shell is to create a symlink to `main.py` by running

`sudo ln -s /path/to/main.py /usr/local/bin/aws-openapi-lint`

or simply add the script directory's path to `$PATH` by running

`PATH=$PATH:/path/to/mainpy/dir`

# Usage

Run `aws-openapi-lint path/to/spec.yml`.

The program terminates with exit code equal to the amount of violations found.