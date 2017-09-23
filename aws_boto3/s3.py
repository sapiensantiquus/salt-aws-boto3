from botocore.exceptions import ClientError
from aws_boto3.common import get_client, AWS_REGION


def s3_ensure_bucket(bucket_name, region=None, acl=None, grant_full_control=None,
                     grant_read=None, grant_read_acp=None, grant_write=None, grant_write_acp=None):
    if region is None:
        region = AWS_REGION

    status = {
        'bucket_name': bucket_name,
        'region': region,
        'status': None
    }

    kwargs = {
        'Bucket': bucket_name,
        'CreateBucketConfiguration': {
            'LocationConstraint': region
        }
    }
    if acl:
        kwargs['ACL'] = acl
    if grant_full_control:
        kwargs['GrantFullControl'] = grant_full_control
    if grant_read:
        kwargs['GrantRead'] = grant_read
    if grant_read_acp:
        kwargs['GrantReadACP'] = grant_read_acp
    if grant_write:
        kwargs['GrantWrite'] = grant_write
    if grant_write_acp:
        kwargs['GrantWriteACP'] = grant_write_acp

    try:
        client = get_client('s3', region=region)
        response = client.create_bucket(**kwargs)
        status['status'] = 'Created'
        status['response'] = response
    except ClientError as e:
        if 'BucketAlreadyOwnedByYou' not in str(e):
            raise e
        status['status'] = 'BucketAlreadyOwnedByYou'
    return status
