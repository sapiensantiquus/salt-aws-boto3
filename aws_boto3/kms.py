import logging

import jmespath

from aws_boto3.common import get_client

logger = logging.getLogger(__name__)


def __alias_name(alias):
    if not alias.startswith('alias/'):
        return 'alias/{}'.format(alias)
    return alias


def get_alias_arn(alias):
    client = get_client('kms')
    pager = client.get_paginator('list_aliases').paginate()
    query = "Aliases[?AliasName == '{}'].AliasArn".format(alias)
    for page in pager:
        result = jmespath.search(query, page)
        if result:
            return result
    return False


def kms_list_keys(client=None, region=None):
    client = get_client('kms')
    response = client.list_keys()
    return [key['KeyId'] for key in response['Keys']]


def kms_create_key(description, policy=None, bypass_policy_lockout_safety_check=False,
                   key_usage='ENCRYPT_DECRYPT', origin='AWS_KMS', tags=[]):
    create_key_params = {
        'Description': description,
        'BypassPolicyLockoutSafetyCheck': bypass_policy_lockout_safety_check,
        'KeyUsage': key_usage,
        'Origin': origin,
        'Tags': tags
    }
    if policy:
        create_key_params['Policy'] = policy
    logger.debug({'create_key_params': create_key_params})
    client = get_client('kms')
    return client.create_key(**create_key_params).get('KeyMetadata')


def kms_create_alias(alias_name, key_id):
    alias_name = __alias_name(alias_name)
    create_alias_params = {
        'AliasName': alias_name,
        'TargetKeyId': key_id
    }
    logger.debug({'create_alias_params': create_alias_params})
    try:
        client = get_client('kms')
        client.create_alias(**create_alias_params)
    except Exception as e:
        logger.error(str(e))
        return False
    return True


def kms_ensure_key(alias_name, description=None, policy=None, bypass_policy_lockout_safety_check=False,
                   key_usage='ENCRYPT_DECRYPT', origin='AWS_KMS', tags=[]):
    alias_name = __alias_name(alias_name)
    key_alias = get_alias_arn(alias_name)

    if not key_alias:
        logger.debug('[kms_ensure_key] key does not exist... creating it...')
        if description is None:
            description = alias_name

        key = kms_create_key(
            description=description,
            policy=policy,
            bypass_policy_lockout_safety_check=bypass_policy_lockout_safety_check,
            key_usage=key_usage,
            origin=origin,
            tags=tags
        )
        if kms_create_alias(alias_name, key['KeyId']):
            # need to get the new alias arn
            key_alias = get_alias_arn(alias_name)

    return key_alias
