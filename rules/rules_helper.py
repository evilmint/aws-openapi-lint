import re


def find_path_params(path):
    path_params = re.findall(r'(\{[a-zA-Z _\-0-9]+\})', path)
    path_params = map(lambda x: x.replace('{', '').replace('}', ''), path_params)
    return path_params


def contains_apigateway_integration(path_verb):
    return 'x-amazon-apigateway-integration' in path_verb


def contains_request_parameters(path_verb):
    return 'requestParameters' in path_verb['x-amazon-apigateway-integration']


def get_path_verbs(spec, path):
    verbs = spec['paths'][path].keys()
    return map(lambda x: x.lower(), verbs)


def get_apigateway_integration(spec, path, verb):
    return spec['paths'][path][verb]['x-amazon-apigateway-integration']


def path_contains_verb(spec, path, verb):
    return verb in spec['paths'][path]


def get_path_headers(spec, path):
    verbs = spec['paths'][path].keys()

    header_parameters = []
    for verb in verbs:
        if 'parameters' not in spec['paths'][path][verb]:
            continue

        parameters = filter(lambda p: p['in'] == 'header', spec['paths'][path][verb]['parameters'])
        parameters = map(lambda p: p['name'], parameters)
        header_parameters += parameters

    return header_parameters


def integration_response_contains_parameters(spec, path, verb, response, parameters):
    response_params = get_apigateway_integration(spec, path, verb)['responses'][response]['responseParameters']
    return parameters in response_params


def get_integration_response_parameters(spec, path, verb, response):
    return get_apigateway_integration(spec, path, verb)['responses'][response]['responseParameters']


def get_integration_verb(spec, path, verb):
    return get_apigateway_integration(spec, path, verb)['httpMethod']


def authorizer_referenced_in_request_params(spec, path, verb) -> bool:
    request_params = get_apigateway_integration(spec, path, verb)['requestParameters']

    for request_param in request_params.values():
        if request_param.startswith('context.authorizer'):
            return True
    return False


def has_security_components(spec, path, verb):
    has_security = 'security' in spec['paths'][path][verb]
    return has_security and len(spec['paths'][path][verb]['security']) > 0
