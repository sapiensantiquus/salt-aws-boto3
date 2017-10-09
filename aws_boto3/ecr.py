import logging

from aws_boto3.common import boto_client, object_search

logger = logging.getLogger(__name__)


@boto_client('ecr')
def get_repo_attr(name, return_attr='repositoryArn', region=None, client=None):
    return object_search(
        client=client,
        paginator='describe_repositories',
        query="repositories[?repositoryName == '{}'].{}".format(name, return_attr),
        return_single=True
    )


@boto_client('ecr')
def ecr_ensure_repo(repo_name, region=None, client=None):
    response = False
    repo_arn = get_repo_attr(repo_name)
    if not repo_arn:
        try:
            response = client.create_repository(repositoryName=repo_name)
            repo_arn = response['repository']['repositoryArn']
        except Exception:
            raise
    return {'repositoryArn': repo_arn}


@boto_client('ecr')
def ecr_absent_repo(repo_name, force=False, registry_id=None, region=None, client=None):
    response = False
    repo_arn = get_repo_attr(repo_name)
    if repo_arn:
        kwargs = {
            'repositoryName': repo_name,
            'force': force
        }
        if registry_id:
            kwargs['registryId'] = registry_id
        try:
            client.delete_repository(**kwargs)
            response = {'RepositoryAbsent': repo_name}
        except Exception as e:
            response = {'ERROR': str(e)}
            logger.exception(str(e))
    else:
        response = {'RepositoryAbsent': repo_name}
    return response
