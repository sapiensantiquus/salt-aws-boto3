import logging

from aws_boto3.common import get_client

logger = logging.getLogger(__name__)


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
