from botocore.exceptions import ClientError

from aws_boto3.common import get_client


def ddb_get_table(table_name, region=None):
    table = False
    try:
        table = get_client('dynamodb', region=region).describe_table(TableName=table_name)
    except ClientError:
        table = False
    return table
