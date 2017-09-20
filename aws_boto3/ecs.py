from aws_boto3.common import get_client


def ecs_ensure_cluster(cluster_name):
    cluster_arn = None
    try:
        client = get_client('ecs')
        response = client.create_cluster(clusterName=cluster_name)
        cluster_arn = response['cluster']['clusterArn']
    except Exception:
        raise
    return cluster_arn
