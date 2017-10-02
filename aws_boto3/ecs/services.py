import logging

from botocore.exceptions import ClientError

from aws_boto3.common import get_client
from aws_boto3.ecs.tasks import ecs_ensure_register_task


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
