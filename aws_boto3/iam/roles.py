import jmespath
from botocore.exceptions import ClientError

from aws_boto3.common import dict_to_str, get_client, object_search


def get_role_arn(name):
    return object_search(
        client=get_client('iam'),
        paginator='list_roles',
        query="Roles[?RoleName == '{}'].Arn".format(name),
        return_single=True
    )


def get_attached_policies(name):
    return jmespath.search(
        "AttachedPolicies[*].PolicyName",
        get_client('iam').list_attached_role_policies(RoleName=name)
    )


def create_role(name, assume_role_policy_document, path=None, description=None):
    kwargs = {
        'RoleName': name,
        'AssumeRolePolicyDocument': dict_to_str(assume_role_policy_document)
    }
    if path:
        kwargs['Path'] = path
    if description:
        kwargs['Description'] = description

    client = get_client('iam')
    role = client.create_role(**kwargs)
    return role['Role'].get('Arn')


def attach_role_policy(role_name, policy_arn):
    kwargs = {
        'RoleName': role_name,
        'PolicyArn': policy_arn
    }
    response = False
    try:
        client = get_client('iam')
        client.attach_role_policy(**kwargs)
        response = get_attached_policies(role_name)
    except ClientError as e:
        response = {'ERROR': str(e), 'kwargs': kwargs}
        # response = False
    return response
