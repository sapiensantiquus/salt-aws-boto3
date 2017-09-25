# Lambda


## `lambda_sync_function`


Property               | Type     | Required | Default           | Description
-----------------------|----------|----------|-------------------|---------------
function_name          | string   | yes      |                   | The friendly name of the function.
handler                | string   | yes      |                   |
role_name              | string   | yes      |                   |
code                   | dict     | yes      |                   |
region                 | string   | no       | `us-east-1`       | The AWS region
runtime                | string   | yes      | `python2.7`       |
description            | string   | no       |                   |
timeout                | int      | no       | 3                 |
memory_size            | int      | no       | 128               |
publish                | boolean  | no       | True              |
vpc_config             | dict     | no       |                   |
dead_letter_config     | string   | no       |                   |
environment            | string   | no       |                   |
kms_key_arn            | string   | no       |                   |
tracing_config         | string   | no       |                   |
tags                   | list     | no       |                   |


#### Example

```yaml
ensure-lambda-function:
  module.run:
    - name: aws_boto3.lambda_sync_function
    - function_name: my-function
    - handler: package.function_name
    - code: package.function_name
        S3Bucket: the-bucket
        S3Key: path/to/s3-object.zip
    - region: "{{ aws_region }}"
```
