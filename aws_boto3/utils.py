from aws_boto3.common import get_client


def run_client(service, function, region=None, payload=None):
    client = get_client(service, region=region)
    fn = getattr(client, function)
    return fn(**payload)
