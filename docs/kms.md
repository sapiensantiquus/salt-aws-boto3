# <a name="kms"></a> KMS


## `kms_create_key`

Command:

```bash
salt '*' aws_boto3.kms_create_alias alias_name='alias/kms/mykey' key_id=<kms-key-id>
```

Response:

```yaml
minion_id:
    True
```

## `kms_create_key`

Command:

```bash
salt '*' aws_boto3.kms_create_key description='mykey' [, policy=None, bypass_policy_lockout_safety_check=False, key_usage='ENCRYPT_DECRYPT', origin='AWS_KMS', tags=[]]
```

Response:

```yaml
minion_id:
    AWSAccountId:
        <aws_account_id>
    Arn:
        arn:aws:kms:us-east-1:<aws_account_id>:key/<kms-key-id>
    CreationDate:
        ¸20170917T19:39:58.546000
    Description:
        mykey
    Enabled:
        True
    KeyId:
        <kms-key-id>
    KeyManager:
        CUSTOMER
    KeyState:
        Enabled
    KeyUsage:
        ENCRYPT_DECRYPT
    Origin:
        AWS_KMS
```

## `kms_list_keys`

Command:

```bash
salt '*' aws_boto3.kms_list_keys
```

Response:

```yaml
minion_id:
    - kms-key-id
```
