# ECS


## `ecs_ensure_config`


Property              | Type     | Required | Default     | Description
----------------------|----------|----------|-------------|-------------------------------------
cluster_definition    | dict     | yes      |             | [boto3 docs](http://boto3.readthedocs.io/en/latest/reference/services/ecs.html#ECS.Client.create_cluster)
services              | list     | no       |             | [boto3 docs](http://boto3.readthedocs.io/en/latest/reference/services/ecs.html#ECS.Client.create_service)
services.task         | dict     | no       |             | [boto3 docs](http://boto3.readthedocs.io/en/latest/reference/services/ecs.html#ECS.Client.register_task_definition)
region                | string   | no       | us-east-1   | The AWS region


#### Examples

```yaml
ensure-cluster:
  module.run:
    - name: aws_boto3.ecs_ensure_config
    - cluster_definition: dict
    - services: list
```


**python example:**

```python
cluster = ecs_ensure_config({
    'cluster_definition': {
        'clusterName': 'clustername'
    },
    'services': [
        {
            'service_definition': {
                'serviceName': 'the-service-name',
                'desiredCount': 1
            },
            'task': {
                'task_definition': {
                    'family': 'task-family-name',
                    'containerDefinitions': [
                        {
                            'name': 'container-name',
                            'image': ecr.get_repo_attr('my-ecr-image-name', return_attr='repositoryUri'),
                            'memory': 256
                        }
                    ]
                }
            }
        }
    ]
})
```
