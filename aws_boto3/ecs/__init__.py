from aws_boto3.common import get_client
from aws_boto3.ecs.services import ecs_ensure_service


def ecs_ensure_cluster(cluster, region=None):
    client = get_client('ecs', region=region)
    cluster_definition = cluster['cluster_definition']
    response = client.create_cluster(**cluster_definition)

    cluster_arn = response['cluster']['clusterArn']
    service_response = None
    if 'services' in cluster:
        services = cluster['services']
        response['services'] = []
        for service in services:
            service['service_definition']['cluster'] = cluster_arn
            service_response = ecs_ensure_service(service, region)
            response['services'].append(service_response)

    return response
