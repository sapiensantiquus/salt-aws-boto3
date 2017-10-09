import jmespath
from botocore.exceptions import ClientError

from aws_boto3.common import boto_client, dict_to_str, object_search


@boto_client('iam')
def get_role_arn(name, region=None, client=None):
    return object_search(
        client=client,
        paginator='list_roles',
        query="Roles[?RoleName == '{}'].Arn".format(name),
        return_single=True
    )


@boto_client('iam')
def get_attached_policies(name, region=None, client=None):
    return jmespath.search(
        "AttachedPolicies[*].PolicyName",
        client.list_attached_role_policies(RoleName=name)
    )


@boto_client('iam')
def create_role(name, assume_role_policy_document, path=None, description=None, region=None, client=None):
    kwargs = {
        'RoleName': name,
        'AssumeRolePolicyDocument': dict_to_str(assume_role_policy_document)
    }
    if path:
        kwargs['Path'] = path
    if description:
        kwargs['Description'] = description

    role = client.create_role(**kwargs)
    return role['Role'].get('Arn')


@boto_client('iam')
def attach_role_policy(role_name, policy_arn, region=None, client=None):
    kwargs = {
        'RoleName': role_name,
        'PolicyArn': policy_arn
    }
    response = False
    try:
        client.attach_role_policy(**kwargs)
        response = get_attached_policies(role_name)
    except ClientError as e:
        response = {'ERROR': str(e), 'kwargs': kwargs}
        # response = False
    return response
