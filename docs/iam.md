# <a name="iam"></a> IAM


## `iam_ensure_role`


Property                    | Type     | Required | Default     | Description
----------------------------|----------|----------|-------------|---------------
role_name                   | string   | yes      |             | The friendly name of the role.
assume_role_policy_document | string   | yes      |             | The trust relationship policy document that grants an entity permission to assume the role.
path                        | string   | no       |             | The path to the role.
description                 | string   | no       |             | A description of the role.
attach_policy_name          | string   | no       |             | The friendly name of the policy.
attach_policy_path          | string   | no       |             | The path for the policy.
attach_policy_description   | string   | no       |             | A friendly description of the policy.
attach_policy_document      | mapping  | no       |             | The JSON policy document that you want to use as the content for the new policy.


#### Example

```yaml
ensure-test-role:
  module.run:
    - name: aws_boto3.iam_ensure_role
    - role_name: credstash-write-role
    - description: 'Role used to write credstash secrets'
    - assume_role_policy_document: '{"Version": "2012-10-17","Statement": {"Effect": "Allow","Principal": {"Service": "ecs.amazonaws.com"},"Action": "sts:AssumeRole"}}'
    - attach_policy_name: credstash-write-policy
    - attach_policy_description: 'Policy used to write credstash secrets'
    - attach_policy_document:
        Version: "2012-10-17"
        Statement:
        - Action:
          - "kms:GenerateDataKey"
          Effect: Allow
          Resource: "arn:aws:kms:{AWS_REGION}:{AWS_ACCOUNT_ID}:alias/credstash"
        - Action:
          - "dynamodb:PutItem"
          Effect: Allow
          Resource: "arn:aws:dynamodb:{AWS_REGION}:{AWS_ACCOUNT_ID}:table/credential-store"
```
