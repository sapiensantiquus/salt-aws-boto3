import json
import os
from collections import Mapping

import boto3
import jmespath

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')


def get_client(name, client_type='client', region=None, *args, **kwargs):
    if region is None:
        region = AWS_REGION
    fn = getattr(boto3, client_type)
    return fn(name, region_name=region, **kwargs)


def object_search(client, paginator, query, return_single=False):
    pager = client.get_paginator(paginator).paginate()
    for page in pager:
        result = jmespath.search(query, page)
        if result:
            if return_single:
                result = result.pop()
            return result
    return False


def dict_to_str(thing):
    if isinstance(thing, Mapping):
        return json.dumps(thing)
    return thing
