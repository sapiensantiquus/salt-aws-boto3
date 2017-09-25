from aws_boto3.dynamodb import ddb_get_table
from aws_boto3.ecr import ecr_absent_repo, ecr_ensure_repo
from aws_boto3.iam import iam_ensure_role
from aws_boto3.kms import kms_ensure_key
from aws_boto3.lambdas import lambda_sync_function
from aws_boto3.s3 import s3_ensure_bucket
