import re
import sys
import subprocess

import time
from urllib3.exceptions import HTTPError

from riseml.errors import handle_error
from riseml.client import AdminApi, ApiClient
from riseml.client.rest import ApiException
from riseml.client_config import get_api_url, get_api_key, write_config, get_api_server, get_sync_url
from riseml.util import call_api, print_table, TableRowDelimiter, get_rsync_path
from riseml.client import Configuration
from riseml.user import get_user


def add_user_parser(parser):
    subparser = parser.add_parser('user', help="modify users")
    subsubparsers = subparser.add_subparsers()
    add_create_parser(subsubparsers)
    add_update_parser(subsubparsers)
    add_disable_parser(subsubparsers)
    add_list_parser(subsubparsers)
    add_display_parser(subsubparsers)
    add_login_parser(subsubparsers)
    def run(args):
        subparser.print_usage()
    subparser.set_defaults(run=run)


def add_create_parser(subparsers):
    parser = subparsers.add_parser('create', help="create user")
    parser.add_argument('--username', help="a person's username", required=True)
    parser.add_argument('--email', help="a person's email", required=True)
    parser.set_defaults(run=run_create)


def add_update_parser(subparsers):
    parser = subparsers.add_parser('update', help="update user")
    parser.add_argument('--username', help="the person's username", required=True)
    parser.add_argument('--email', help="the person's new email", required=True)
    parser.set_defaults(run=run_update)


def add_disable_parser(subparsers):
    parser = subparsers.add_parser('disable', help="disable user")
    parser.add_argument('username', help="a person's username")
    parser.set_defaults(run=run_disable)


def add_display_parser(subparsers):
    parser = subparsers.add_parser('display', help="show user info")
    parser.add_argument('username', help="a person's username")
    parser.set_defaults(run=run_display)


def add_list_parser(subparsers):
    parser = subparsers.add_parser('list', help="list users")
    parser.set_defaults(run=run_list)


def add_login_parser(subparsers):
    parser = subparsers.add_parser('login', help="login new user")
    parser.add_argument('--api-host', help="Hostname/IP and port of RiseML API server")
    parser.add_argument('--api-key', help="RiseML API key")
    parser.set_defaults(run=run_login)


def run_login(args):
    print('Configuring new user login. This will overwrite your existing configuration. \n')
    try:
        api_key, host, cluster_config = login_api(args)
        print()

        write_config(api_key, host, cluster_config)
        print('Login succeeded, config updated.')
    except (KeyboardInterrupt, EOFError) as e:
        print('Aborting login. Configuration unchanged.')
        sys.exit(1)


def login_api(args):
    api_host = args.api_host
    if not args.api_host:
        current_api_server = get_api_server()
        default = re.match(r'^http://(.*)$', current_api_server).group(1) if current_api_server else ''
        print('Please provide the DNS name or IP of your RiseML API server.')
        if default:
            print('Default: {}'.format(default))
        else:
            print('Example: 54.131.125.42:31213')
        while True:
            api_host = input('--> ').strip() or default
            if api_host:
                break
            print('You need to enter a value!')
        print()

    api_key = args.api_key
    if not args.api_key:
        default = get_api_key()
        print('Please provide your API key.')
        if default:
            print('Default: {}'.format(default))
        else:
            print('Example: krlo2oxrtd2084zs7jahwyqu12b7mozg')
        while True:
            api_key = input('--> ').strip() or default or ''
            if api_key:
                break
            print('You need to enter a value!')
        print()

    host = api_host.split(':')[0]
    cluster_config = check_api_config(get_api_url(api_host), api_key)
    check_sync_config('rsync://%s:%s/sync' % (host, cluster_config.ports.sync))
    return api_key, host, cluster_config


def check_sync_config(rsync_url, timeout=20):
    print('Checking connection to sync server %s for at most %ss... ' % (rsync_url, timeout), end='', flush=True)

    start = time.time()
    while True:
        sync_cmd = [get_rsync_path(),
                '--dry-run',
                '--timeout=10',
                '--contimeout=10',
                '.',
                rsync_url]
        proc = subprocess.Popen(sync_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        res = proc.wait()
        if res != 0:
            if time.time() - start < timeout:
                time.sleep(1)
                continue
            else:
                handle_error('Could not connect to sync server: %s' % proc.stdout.read().decode('utf-8'))
        else:
            print('Success!')
            break


def check_api_config(api_url, api_key, timeout=180):
    print('Trying to login to %s with API key \'%s\' for at most %ss... ' % (api_url, api_key, timeout), end='', flush=True)
    config = Configuration()
    old_api_host = config.host
    old_api_key = config.api_key['api_key']
    config.host = api_url
    config.api_key['api_key'] = api_key
    api_client = ApiClient()
    client = AdminApi(api_client)
    start = time.time()
    while True:
        try:
            cluster_config = client.login_user()
            print('Success!')
            config.api_key['api_key'] = old_api_key
            config.host = old_api_host
            return cluster_config
        except ApiException as exc:
            if exc.reason == 'UNAUTHORIZED':
                print(exc.status, 'Unauthorized - wrong api key?')
                sys.exit(1)
            elif time.time() - start < timeout:
                time.sleep(1)
                continue
            else:
                print(exc.status, exc.reason)
                sys.exit(1)
        except HTTPError as e:
            if time.time() - start < timeout:
                time.sleep(1)
                continue
            else:
                print('Unable to connect to %s ' % api_url)
                # all uncaught http errors goes here
                print(e.reason)
                sys.exit(1)


def run_create(args):
    api_client = ApiClient()
    client = AdminApi(api_client)
    validate_username(args.username)
    validate_email(args.email)
    user = call_api(lambda: client.create_user(username=args.username, email=args.email))[0]
    print('Created user %s' % user.username)
    print(' email: %s' % user.email)
    print(' api_key: %s' % user.api_key_plaintext)


def run_update(args):
    api_client = ApiClient()
    client = AdminApi(api_client)
    validate_username(args.username)
    validate_email(args.email)
    user = call_api(lambda: client.update_user(username=args.username, email=args.email))
    print('Updated user {}'.format(user.username))
    print(' email: {}'.format(user.email))


def run_list(args):
    api_client = ApiClient()
    client = AdminApi(api_client)
    users = call_api(lambda: client.get_users())
    rows = []
    for u in users:
        rows.append([u.username, u.email, str(u.is_enabled)])

    print_table(
        header=['Username', 'Email', 'Enabled'],
        min_widths=[12, 6, 9],
        column_spaces=2,
        rows=rows
    )


def run_display(args):
    api_client = ApiClient()
    client = AdminApi(api_client)
    users = call_api(lambda: client.get_users(username=args.username))
    if not users:
        print('User %s not found.' % args.username)
    else:
        user = users[0]
        print('username: %s' % user.username)
        print('email: %s' % user.email)
        print('api_key: %s' % user.api_key_plaintext)


def run_disable(args):
    sys.stdout.write("Are you sure you want to disable user %s? [y/n]: " % args.username)
    def user_exit():
        print("Apparently not...")
        exit(0)
    try:
        choice = input()
    except KeyboardInterrupt:
        user_exit()
    if choice.strip() != 'y':
        user_exit()
    api_client = ApiClient()
    client = AdminApi(api_client)
    call_api(lambda: client.delete_user(username=args.username))
    print('User %s disabled.' % args.username)


def validate_username(username):
    if not re.match(r'^[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9]$', username):
        handle_error('Username must start and end with an alphanumeric character and may additionally consist out of hyphens inbetween.')

def validate_email(email):
    if '@' not in email:
        handle_error('Invalid email')
