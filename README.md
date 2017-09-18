# salt-aws-boto3

Use boto3 for AWS orchestration with Salt.

## Setup

* copy `aws_boto3` to your salt modules directory
* copy `pip_deps.sls` to your salt states directory
* run `salt '*' state.apply pip_deps`
* run `salt '*' saltutil.sync_modules`


## Documentation

* [KMS](./docs/kms.md)
