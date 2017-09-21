# DynamoDB


## `ddb_get_table`


Property   | Type     | Required | Default     | Description
-----------|----------|----------|-------------|-------------------------------------
table_name | string   | yes      |             | The friendly name of the table.
region     | string   | no       | us-east-1   | The AWS region


#### Example

```python
from aws_boto3 import ddb_get_table

if not ddb_get_table('table-name', region='us-west-2'):
    do some things
```
