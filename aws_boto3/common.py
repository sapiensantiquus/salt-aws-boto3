import json
import os
from collections import Mapping
from functools import wraps
from inspect import getargspec

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


def boto_client(service_name, client_type='client', region=AWS_REGION,
                client_param_name='client', region_param_name='region'):
    def _get_client(func):
        @wraps(func)
        def make_client(*args, **kwargs):
            fn_spec = getargspec(func)
            # create a dict with the fn's kwargs and default values
            params = dict(
                zip(fn_spec.args[-len(fn_spec.defaults):], fn_spec.defaults)
            )

            # update params with arg values and keys
            params.update(dict((zip(fn_spec.args[:len(args)], args))))
            params.update(kwargs)

            if params.get(region_param_name) is None:
                params[region_param_name] = region

            if params.get(client_param_name) is None:
                params[client_param_name] = get_client(
                    service_name,
                    client_type,
                    params[region_param_name]
                )

            return func(**params)
        return make_client
    return _get_client
