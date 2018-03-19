import os
import re
from minio import Minio
from minio.error import InvalidBucketError, NoSuchBucket

from riseml.consts import DEFAULT_CONFIG_NAME
from riseml.client_config import get_user
from riseml.configs import get_project_name
from ...client_config import get_minio_data_host, get_minio_output_host, get_minio_access_key, get_minio_secret_key
from ...errors import handle_error

def is_local(path_or_uri):
    return re.match(r'^[^:]+://', path_or_uri) is None

def is_local_dir(path):
    return os.path.isdir(path)

def is_remote(path_or_uri):
    return not is_local(path_or_uri)

def is_remote_dir(uri):
    storage, bucket, path = parse_uri(uri)
    if not bucket:
        return True
    elif not path:
        return True
    else:
        exact_object = get_exact_object(storage, bucket, path, raise_exc=False)
        return exact_object.is_dir if exact_object else False

def with_trailing_slash(string):
    return string if string.endswith('/') else string + '/'

def without_trailing_slash(string):
    return string[:-1] if string.endswith('/') else string

def get_minio_host(storage):
    if storage == 'data':
        return get_minio_data_host()
    elif storage == 'output':
        return get_minio_output_host()
    else:
        handle_error('Unknown storage type (%s).' % storage)

def get_minio_client(storage, cache={}):
    host = get_minio_host(storage)
    if not host in cache:
        cache[host] = Minio(host,
                            access_key=get_minio_access_key(),
                            secret_key=get_minio_secret_key(),
                            secure=False)
    return cache[host]

def expand_uri(uri):
    if re.match(r'^output://~(/.*)?$', uri):
        home_dir = 'output://{}/{}'.format(
            get_user(),
            get_project_name(DEFAULT_CONFIG_NAME))
        uri = uri.replace('output://~', home_dir)
    return uri

def build_uri(storage, bucket=None, path=None):
    uri = storage + '://'
    if bucket:
        uri += bucket
        if path:
            uri += '/' + path
    return uri

def parse_uri(uri):
    match = re.match(r'^(data|output)://(?:([^/]+)(?:/(.*)?)?)?$', uri)
    if not match:
        handle_error('Cannot handle data uri (%s).' % uri)
    storage, bucket, path = match.groups()
    return storage, bucket, path

def get_file_name(object_name):
    name = re.findall(r'[^/]+/?$', object_name)
    return name[0]

def get_exact_object(storage, bucket, path, raise_exc=True):
    def is_exact_match(obj):
        return with_trailing_slash(obj.object_name) == with_trailing_slash(path)
    try:
        objects = get_minio_client(storage).list_objects_v2(bucket, without_trailing_slash(path))
        return next((obj for obj in objects if is_exact_match(obj)))
    except (InvalidBucketError, NoSuchBucket, StopIteration):
        if raise_exc:
            handle_path_does_not_exist(build_uri(storage, bucket, path))
        else:
            return None

def get_dir_objects(storage, bucket, path, recursive=False):
    minio_client = get_minio_client(storage)
    objects = minio_client.list_objects_v2(bucket, path, recursive=recursive)
    try:
        for obj in objects:
            yield obj
    except (InvalidBucketError, NoSuchBucket):
        handle_path_does_not_exist(build_uri(storage, bucket, path))

def get_buckets(storage):
    return get_minio_client(storage).list_buckets()

def handle_path_does_not_exist(path):
    handle_error("Path {} does not exist!".format(path))

def handle_no_path_given():
    handle_error("You need to add a path!")
