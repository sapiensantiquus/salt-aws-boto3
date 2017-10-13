from botocore.exceptions import ClientError

from aws_boto3.common import boto_client, object_search

from aws_boto3.iam.roles import get_role_arn


@boto_client('lambda')
def lambda_lookup(name, return_attr='FunctionArn', client=None, region=None):
    return object_search(
        client=client,
        paginator='list_functions',
        query="Functions[?FunctionName == '{}'].{}".format(name, return_attr),
        return_single=True
    )


@boto_client('lambda')
def run_fn(fn_name, payload, client=None, region=None):
    fn = getattr(client, fn_name)
    return fn(**payload)


@boto_client('lambda')
def lambda_create(function_definition, client=None, region=None):
    status = {
        'status': None,
        'exists': False
    }
    try:
        response = client.create_function(**function_definition)
        status['status'] = 'Created'
        status['exists'] = True
        status['response'] = response
    except ClientError as e:
        raise e
    return {'lambda_create': status}


# def publish_version()


def lambda_sync_function(function_name, handler, role_name, code, region=None, runtime='python2.7',
                         description=None, timeout=None, memory_size=None, publish=True,
                         vpc_config=None, dead_letter_config=None, environment=None,
                         kms_key_arn=None, tracing_config=None, tags=None, version=None, alias=None):
    role = get_role_arn(role_name, region=region)
    status = {
        'function_name': function_name,
        'region': region,
        'actions': []
    }
    function_definition = {
        'FunctionName': function_name,
        'Runtime': runtime,
        'Role': role,
        'Handler': handler,
        'Code': code,
        'Publish': publish
    }
    if description:
        function_definition['Description'] = description
    if timeout:
        function_definition['Timeout'] = timeout
    if memory_size:
        function_definition['MemorySize'] = memory_size
    if vpc_config:
        function_definition['VpcConfig'] = vpc_config
    if dead_letter_config:
        function_definition['DeadLetterConfig'] = dead_letter_config
    if environment:
        function_definition['Environment'] = environment
    if kms_key_arn:
        function_definition['KMSKeyArn'] = kms_key_arn
    if tracing_config:
        function_definition['TracingConfig'] = tracing_config
    if tags:
        function_definition['Tags'] = tags

    lambda_arn = lambda_lookup(function_name, region=region)

    if not lambda_arn:
        status['actions'].append(lambda_create(function_definition, region=region))

    if publish:
        publish_response = run_fn(
            'publish_version',
            payload={
                'FunctionName': function_name,
                'Description': version
            },
            region=region
        )
        lambda_version = publish_response.get('Version')
        status['lambda_version'] = lambda_version
        status['actions'].append({'publish_version': publish_response})

        try:
            alias_response = run_fn(
                'create_alias',
                payload={
                    'FunctionName': function_name,
                    'Name': alias,
                    'FunctionVersion': lambda_version
                },
                region=region
            )
            status['alias'] = alias
            status['actions'].append({'create_alias': alias_response})
        except ClientError as e:
            if 'Alias already exists' not in str(e):
                # TODO
                raise e
            status['alias'] = alias
    return status
