import logging

from botocore.exceptions import ClientError

from aws_boto3.common import get_client


def ecs_ensure_register_task(task, region=None):
    client = get_client('ecs', region=region)
    return client.register_task_definition(**task['task_definition'])


def ecs_ensure_service(service, region=None):
    task_response = None
    if 'task' in service:
        task = service['task']
        task['cluster_arn'] = service['service_definition']['cluster']
        task['service_name'] = service['service_definition']['serviceName']
        task_response = ecs_ensure_register_task(task, region)
        task_arn = task_response['taskDefinition']['taskDefinitionArn']
        service['service_definition']['taskDefinition'] = task_arn

    client = get_client('ecs', region=region)
    response = None
    create_failed = False

    try:
        response = client.create_service(**service['service_definition'])
    except ClientError:
        logging.warn("Failed to create service. Attempting to update...")
        create_failed = True

    if create_failed:
        service_def = service['service_definition']
        wanted_keys = ['cluster', 'desiredCount', 'taskDefinition', 'deploymentConfiguration']
        update_service_def = dict((k, service_def[k]) for k in wanted_keys if k in service_def)
        update_service_def['service'] = service_def['serviceName']
        response = client.update_service(**update_service_def)

    if 'task' in service:
        response['task'] = task_response

    return response


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
