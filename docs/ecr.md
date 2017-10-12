# ECR


## `ecr_ensure_repo`


Property    | Type        | Required | Default     | Description
------------|-------------|----------|-------------|-------------------------------------
repo_name   | string      | yes      |             | The friendly name of the repository.
region      | string      | no       | us-east-1   | The AWS region
policy      | string/dict | no       |             | IAM policy specifying permissions for this repo


#### Example

```yaml
ensure-test-repo:
  module.run:
    - name: aws_boto3.ecr_ensure_repo
    - repo_name: foo
```


## `ecr_absent_repo`
(repo_name, =False, registry_id=None)

Property    | Type     | Required | Default     | Description
------------|----------|----------|-------------|-------------------------------------
repo_name   | string   | yes      |             | The friendly name of the repository.
force       | boolean  | no       | False       | Force the deletion of the repository if it contains images.
registry_id | string   | no       |             | The AWS account ID associated with the registry that contains the repository to delete. If you do not specify a registry, the default registry is assumed.
region      | string   | no       | us-east-1   | The AWS region


#### Example

```yaml
delete-test-repo:
  module.run:
    - name: aws_boto3.ecr_absent_repo
    - repo_name: foo
```
