from . import util

def add_rm_parser(subparsers):
    parser = subparsers.add_parser('rm', help="list files in data or output storage")
    parser.add_argument('files', metavar='file', help='uri/path to file(s) to remove', nargs='+')
    parser.set_defaults(run=run_rm)

def run_rm(args):
    for uri in args.files:
        storage, bucket, path = util.parse_uri(util.expand_uri(uri))
        if not bucket:
            util.handle_no_path_given()
        elif not path:
            delete_bucket(storage, bucket)
        else:
            exact_match = util.get_exact_object(storage, bucket, path)
            if exact_match.is_dir:
                delete_dir(storage, bucket, exact_match.object_name)
            else:
                delete_file(storage, bucket, path)

def delete_bucket(storage, bucket):
    delete_dir(storage, bucket, '')
    print("Deleting {}".format(util.build_uri(storage, bucket)))
    util.get_minio_client(storage).remove_bucket(bucket)

def delete_dir(storage, bucket, path):
    objects = util.get_dir_objects(storage, bucket, path, recursive=True)
    for obj in objects:
        delete_file(storage, bucket, obj.object_name)

def delete_file(storage, bucket, path):
    print("Deleting {}".format(util.build_uri(storage, bucket, path)))
    util.get_minio_client(storage).remove_object(bucket, path)
