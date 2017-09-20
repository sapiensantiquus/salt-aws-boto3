# ECS


## `ecs_ensure_cluster`


Property     | Type     | Required | Default     | Description
-------------|----------|----------|-------------|-------------------------------------
cluster_name | string   | yes      |             | The friendly name of the cluster.


#### Example

```yaml
ensure-cluster:
  module.run:
    - name: aws_boto3.ecs_ensure_cluster
    - cluster_name: foo
```
