from .util import get_minio_client, parse_uri, with_trailing_slash, get_file_name

def add_ls_parser(subparsers):
    parser = subparsers.add_parser('ls', help="list files in data or output storage")
    parser.add_argument('uri', help='uri/path to list', nargs='?')
#    parser.add_argument('-r', '--recursive', help="list recursively", action="store_true")
    parser.set_defaults(run=run_ls)

def run_ls(args):
    if not args.uri:
        print_dir_entry_row(None, 'STORAGE', "data://")
        print_dir_entry_row(None, 'STORAGE', "output://")
    else:
        storage, bucket, path = parse_uri(args.uri)
        minio_client = get_minio_client(storage)
        if not bucket:
            buckets = minio_client.list_buckets()
            for bucket in buckets:
                print_dir_entry_row(bucket.creation_date, 'DIR', bucket.name + '/')
        elif not path:
            buckets = [bucket for bucket in minio_client.list_buckets()]
            exact_bucket_match = next((bc for bc in buckets if bc.name == bucket), None)
            if exact_bucket_match:
                list_bucket_objects(minio_client, bucket, '')
            else:
                for bc in buckets:
                    if bc.name.startswith(bucket):
                        print_dir_entry_row(bc.creation_date, 'DIR', bc.name + '/')
        else:
            list_bucket_objects(minio_client, bucket, path)

def print_dir_entry_row(datetime, size_or_type, name):
    print('{:20} {:>14} {}'.format(
        datetime.strftime("%Y-%m-%d %H:%M:%S") if datetime else '',
        size_or_type,
        name))

def list_bucket_objects(minio_client, bucket, path):
    objects = [obj for obj in minio_client.list_objects_v2(bucket, path)]
    exact_dir_match = next((obj for obj in objects if obj.object_name == with_trailing_slash(path)), None)
    if exact_dir_match:
        objects = [obj for obj in minio_client.list_objects_v2(bucket, exact_dir_match.object_name)]
    objects.sort(key=lambda obj: not obj.object_name.endswith('/'))
    for obj in objects:
        print(obj)
        print_dir_entry_row(obj.last_modified, obj.size or 'DIR', get_file_name(obj.object_name))
