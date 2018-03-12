from minio.error import NoSuchBucket

from ...errors import handle_error
from .util import get_minio_client, parse_uri, build_uri, handle_path_does_not_exists, handle_no_path_given

def add_rm_parser(subparsers):
    parser = subparsers.add_parser('rm', help="list files in data or output storage")
    parser.add_argument('files', metavar='file', help='uri/path to file(s) to remove', nargs='+')
    parser.set_defaults(run=run_rm)

def run_rm(args):
    for uri in args.files:
        storage, bucket, path = parse_uri(uri)
        minio_client = get_minio_client(storage)
        if not bucket:
            handle_no_path_given()
        elif not path:
            if minio_client.bucket_exists(bucket):
                objects = minio_client.list_objects_v2(bucket, '', recursive=True)
                for obj in objects:
                    delete(storage, bucket, obj.object_name)
                delete(storage, bucket)
            else:
                handle_path_does_not_exists()
        else:
            delete(storage, bucket, path)

def delete(storage, bucket, path=None):
    minio_client = get_minio_client(storage)
    print("Deleting {}".format(build_uri(storage, bucket, path)))
    try:
        if path:
            minio_client.remove_object(bucket, path)
        else:
            minio_client.remove_bucket(bucket)
    except NoSuchBucket:
        handle_path_does_not_exists()    
