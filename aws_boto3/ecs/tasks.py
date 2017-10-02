from aws_boto3.common import get_client


def ecs_ensure_register_task(task, region=None):
    client = get_client('ecs', region=region)
    return client.register_task_definition(**task['task_definition'])
