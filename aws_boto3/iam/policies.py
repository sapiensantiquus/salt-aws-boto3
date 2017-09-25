from botocore.exceptions import ClientError

from aws_boto3.common import dict_to_str, get_client, object_search
from aws_boto3.lookup import lookup


def get_policy_arn(name, region=None):
    return object_search(
        client=get_client('iam', region=region),
        paginator='list_policies',
        query="Policies[?PolicyName == '{}'].Arn".format(name),
        return_single=True
    )


def create_policy(policy_name, policy_document, description=None, path=None, region=None):
    for statement in policy_document.get('Statement', []):
        if statement.get('Resource'):
            if statement['Resource'].startswith('lookup'):
                lookup_request = statement['Resource'].split(':')
                lookup_request.pop(0)
                statement['Resource'] = lookup(region=region, *lookup_request)

    kwargs = {
        'PolicyName': policy_name,
        'PolicyDocument': dict_to_str(policy_document)
    }
    if path:
        kwargs['Path'] = path
    if description:
        kwargs['Description'] = description

    response = False
    try:
        client = get_client('iam', region=region)
        response = client.create_policy(**kwargs)
        response = response['Policy']['Arn']
    except ClientError as e:
        # return '[ERROR] {}'.format(str(e))
        response = {'ERROR': str(e), 'kwargs': kwargs}
    return response
