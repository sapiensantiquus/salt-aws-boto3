# DynamoDB


## `ddb_get_table`


Property   | Type     | Required | Default     | Description
-----------|----------|----------|-------------|-------------------------------------
table_name | string   | yes      |             | The friendly name of the table.


#### Example

```yaml
credstash-setup:
  cmd.run:
    - name: /usr/local/bin/credstash setup
    - unless: aws_boto3.ddb_get_table
```
