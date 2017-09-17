import boto3

AWS_REGION = 'us-east-1'
# AWS_REGION = __grains__['aws_region']


def get_client(name, client_type='client', region=None, *args, **kwargs):
    if region is None:
        region = AWS_REGION
    fn = getattr(boto3, client_type)
    return fn(name, region_name=region, **kwargs)
