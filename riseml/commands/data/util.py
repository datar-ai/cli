import os
import re
from minio import Minio
from minio.error import NoSuchBucket, NoSuchKey

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
    minio_client = get_minio_client(storage)
    if not bucket:
        return True
    elif not path:
        return True
    else:
        try:
            minio_client.get_object(bucket, with_trailing_slash(path))
        except (NoSuchBucket, NoSuchKey):
            return False
        return True

def with_trailing_slash(string):
    return string if string.endswith('/') else string + '/'

def get_minio_client(storage, cache={}):
    if storage == 'data':
        host = get_minio_data_host()
    elif storage == 'output':
        host = get_minio_output_host()
    else:
        handle_error('Unknown storage type (%s).' % storage)
    if not host in cache:
        cache[host] = Minio(host,
                            access_key=get_minio_access_key(),
                            secret_key=get_minio_secret_key(),
                            secure=False)
    return cache[host]

def build_uri(storage, bucket=None, path=None):
    uri = storage + '://'
    if bucket:
        uri += bucket
        if path:
            uri += '/' + path
    return uri

def parse_uri(uri):
    match = re.match(r'(data|output)://(?:([^/]+)(?:/(.*)?)?)?', uri)
    if not match:
        handle_error('Cannot handle data uri (%s).' % uri)
    storage, bucket, path = match.groups()
    return storage, bucket, path

def get_file_name(object_name):
    name = re.findall(r'[^/]+/?$', object_name)
    return name[0]

def handle_path_does_not_exists():
    handle_error("Path does not exist!")

def handle_no_path_given():
    handle_error("You need to add a path!")
