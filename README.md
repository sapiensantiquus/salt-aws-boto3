# salt-aws-boto3

Use boto3 for AWS orchestration with Salt.

* [Salt Setup](#salt-setup)
* [Python Package Setup](#py-setup)
* [Documentation](#docs)
* [Tests](#tests)

---


## <a name="salt-setup"></a> Salt Setup

* copy `aws_boto3` to your salt modules directory
* copy `pip_deps.sls` to your salt states directory
* run `salt '*' state.apply pip_deps`
* run `salt '*' saltutil.sync_modules`

## <a name="py-setup"></a> Use at as a python package

```bash
[sudo] pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install --editable .
```

## <a name="docs"></a> Documentation

* [DynamoDB](./docs/dynamodb.md)
* [ECR](./docs/ecr.md)
* [ECS](./docs/ecs.md)
* [IAM](./docs/iam.md)
* [KMS](./docs/kms.md)
* [S3](./docs/s3.md)

## <a name="tests"></a> Tests

Run the tests:

```bash
sh run-tests.sh
```
