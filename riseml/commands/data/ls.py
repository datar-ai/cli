from . import util

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
        storage, bucket, path = util.parse_uri(util.expand_uri(args.uri))
        if not bucket:
            buckets = util.get_buckets(storage)
            for bucket in buckets:
                print_dir_entry_row(bucket.creation_date, 'DIR', bucket.name + '/')
        elif not path:
            list_dir_objects(storage, bucket)
        else:
            exact_match = util.get_exact_object(storage, bucket, path)
            if exact_match.is_dir:
                list_dir_objects(storage, bucket, exact_match.object_name)
            else:
                print_dir_entry(exact_match)


def list_dir_objects(storage, bucket, path=None):
    objects = util.get_dir_objects(storage, bucket, path)
    objects = [obj for obj in objects]
    objects.sort(key=lambda obj: not obj.is_dir)
    for obj in objects:
        print_dir_entry(obj)

def print_dir_entry(obj):
    print_dir_entry_row(obj.last_modified, obj.size or 'DIR', util.get_file_name(obj.object_name))

def print_dir_entry_row(datetime, size_or_type, name):
    print('{:20} {:>14} {}'.format(
        datetime.strftime("%Y-%m-%d %H:%M:%S") if datetime else '',
        size_or_type,
        name))
