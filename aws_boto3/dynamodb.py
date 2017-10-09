from botocore.exceptions import ClientError

from aws_boto3.common import boto_client


@boto_client('dynamodb')
def ddb_get_table(table_name, region=None, client=None):
    table = False
    try:
        table = client.describe_table(TableName=table_name)
    except ClientError:
        table = False
    return table
