from aws_boto3.common import boto_client


@boto_client('elb')
def ensure_elb(elb_def, region=None, client=None):
    response = client.create_load_balancer(**elb_def)
    return response['DNSName']
