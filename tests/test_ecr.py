from unittest import TestCase

from mock import patch, MagicMock

from aws_boto3 import ecr


class AwsBoto3EcrTest(TestCase):

    @patch('aws_boto3.ecr.get_client')
    @patch('aws_boto3.ecr.get_repo_attr', return_value=False)
    def test_ecr_ensure_repo(self, get_repo_mock, client_mock):
        client_mock.return_value = MagicMock()
        client_mock.return_value.create_repository = MagicMock()
        client_mock.return_value.create_repository.return_value = {'repository': {'repositoryArn': 'newrepo'}}
        response = ecr.ecr_ensure_repo('foo')
        self.assertEquals(response, {'repositoryArn': 'newrepo'})

    @patch('aws_boto3.ecr.get_client')
    @patch('aws_boto3.ecr.get_repo_attr', return_value='12345')
    def test_ecr_ensure_repo_exists(self, get_repo_mock, client_mock):
        response = ecr.ecr_ensure_repo('foo')
        self.assertEquals(response, {'repositoryArn': '12345'})

    @patch('aws_boto3.ecr.get_client')
    @patch('aws_boto3.ecr.get_repo_attr')
    def test_ecr_absent_repo(self, get_repo_mock, client_mock):
        client_mock.return_value = MagicMock()
        client_mock.return_value.delete_repository = MagicMock()
        client_mock.return_value.delete_repository.return_value = True
        response = ecr.ecr_absent_repo('foo')
        self.assertEquals(response, {'RepositoryAbsent': 'foo'})

    @patch('aws_boto3.ecr.get_client')
    @patch('aws_boto3.ecr.get_repo_attr', return_value=False)
    def test_ecr_absent_repo_not_exists(self, get_repo_mock, client_mock):
        client_mock.return_value = MagicMock()
        client_mock.return_value.delete_repository = MagicMock()
        response = ecr.ecr_absent_repo('deleted')
        self.assertEquals(response, {'RepositoryAbsent': 'deleted'})
