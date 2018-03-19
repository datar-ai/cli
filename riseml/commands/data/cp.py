import os
import itertools
from tqdm import tqdm

from ...util import mkdir_p
from ...errors import handle_error
from . import util

def add_cp_parser(subparsers):
    parser = subparsers.add_parser('cp', help="copy files from/to data or output storage")
    parser.add_argument('sources', metavar='source', help='uri/path to source file(s)', nargs='+')
    parser.add_argument('dest', help='uri/path to destination file/directory')
    parser.set_defaults(run=run_cp)

def run_cp(args):
    dest = util.expand_uri(args.dest)
    sources = ()
    for source in args.sources:
        if util.is_local(source):
            sources = itertools.chain(sources, gather_local_files(source))
        else:
            sources = itertools.chain(sources, gather_remote_files(source))
    
    # TODO: Use generators all way down
    sources = [source for source in sources]
    if len(sources) == 1:
        if (util.is_local(dest) and util.is_local_dir(dest)) or (util.is_remote(dest) and util.is_remote_dir(dest)):
            dest = util.with_trailing_slash(dest) + sources[0].relpath
        copy(sources[0], dest)
    else:
        dest_uri = util.with_trailing_slash(dest)
        for source in sources:
            copy(source, dest_uri + source.relpath)

def copy(source, dest_uri):
    print("Copying {} to {}".format(source.uri, dest_uri))
    if util.is_local(source.uri):
        stream_creator = lambda: open(source.uri, 'rb')
    else:
        stream_creator = lambda: get_download_stream(source.uri)
    with tqdm(total=source.size, unit='byte', unit_scale=True) as pbar:
        with stream_creator() as input_stream:
            if util.is_local(dest_uri):
                store_stream_locally(dest_uri, input_stream, pbar)
            else:
                wrapped_stream = StreamWrapper(input_stream, lambda size: pbar.update(size))
                store_stream_remotely(dest_uri, input_stream, source.size, pbar)


class FileToCopy(object):
    def __init__(self, uri, relpath, size):
        self.uri = uri
        self.relpath = relpath
        self.size = size


def gather_local_files(path):
    if os.path.isdir(path):
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                yield FileToCopy(full_path, os.path.relpath(full_path, path), os.stat(full_path).st_size)
    else:
        yield FileToCopy(path, os.path.basename(path), os.stat(path).st_size)

def store_stream_locally(path, stream, progress_bar):
    dirname = os.path.dirname(path)
    if dirname:
        mkdir_p(dirname)
    with open(path, 'wb') as file_data:
        while True:
            buffer = stream.read(1024 * 1024)
            if len(buffer) == 0:
                break
            file_data.write(buffer)
            progress_bar.update(len(buffer))


class StreamWrapper(object):
    def __init__(self, wrapped_stream, callback):
        self.wrapped_stream = wrapped_stream
        self.callback = callback

    def read(self, size=-1):
        data = self.wrapped_stream.read(size)
        self.callback(size)
        return data


def gather_remote_files(uri):
    uri = util.expand_uri(uri)
    storage, bucket, path = util.parse_uri(uri)
    minio_client = util.get_minio_client(storage)
    if not bucket:
        buckets = minio_client.list_buckets()
        for bucket in buckets:
            yield from gather_remote_dir(storage, bucket, base_uri=uri)
    elif not path:
        yield from gather_remote_dir(storage, bucket, base_uri=uri)
    else:
        exact_match = util.get_exact_object(storage, bucket, path)
        if exact_match.is_dir:
            yield from gather_remote_dir(storage, bucket, exact_match.object_name)
        else:
            yield gather_remote_file(storage, bucket, exact_match)

def gather_remote_dir(storage, bucket, path=None, base_uri=None):
    objects = util.get_dir_objects(storage, bucket, path, recursive=True)
    if not base_uri:
        base_uri = util.build_uri(storage, bucket, path)
    for obj in objects:
        yield gather_remote_file(storage, bucket, obj, base_uri=base_uri)

def gather_remote_file(storage, bucket, obj, base_uri=None):
    full_uri = util.build_uri(storage, bucket, obj.object_name)
    if base_uri:
        relpath = full_uri[len(util.with_trailing_slash(base_uri)):]
    else:
        relpath = util.get_file_name(obj.object_name)
    return FileToCopy(full_uri, relpath, obj.size)

def get_download_stream(uri):
    storage, bucket, path = util.parse_uri(uri)
    minio_client = util.get_minio_client(storage)
    return minio_client.get_object(bucket, path)

def store_stream_remotely(uri, stream, size, progress_bar):
    storage, bucket, path = util.parse_uri(uri)
    if not path:
        handle_error("You need to specify at least one folder!")
    minio_client = util.get_minio_client(storage)
    create_bucket_if_not_exists(minio_client, bucket)
    minio_client.put_object(bucket, path, stream, size,
                            progress=lambda size: progress_bar.update(size))

def create_bucket_if_not_exists(minio_client, bucket, cache=set()):
    if not bucket in cache:
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)
        cache.add(bucket)