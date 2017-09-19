# salt-aws-boto3

Use boto3 for AWS orchestration with Salt.

## Salt Setup

* copy `aws_boto3` to your salt modules directory
* copy `pip_deps.sls` to your salt states directory
* run `salt '*' state.apply pip_deps`
* run `salt '*' saltutil.sync_modules`

## Use at as a python package

```bash
[sudo] pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install --editable .
```

## Documentation

* [IAM](./docs/iam.md)
* [KMS](./docs/kms.md)
