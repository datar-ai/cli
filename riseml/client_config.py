from pathlib import Path
import os
import yaml
import sys
import errno
from .errors import handle_error

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


CONFIG_PATH = '.riseml'
CONFIG_FILE = 'config'

EMPTY_CONFIG = """
current-context: default

contexts:
  - name: default
    context:
      cluster: default
      user: default

clusters:
  - name: default
    cluster:
      api-server: ""
      sync-server: ""
      cluster-id: ""

users:
- name: default
  user:
    api-key: ""
"""

def get_config_file():
    home = str(Path.home())
    return os.path.join(home, CONFIG_PATH, CONFIG_FILE)


def read_config():
    try:
        with open(get_config_file(), 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
            except yaml.scanner.ScannerError as yml_error:
                handle_error('client configuration has invalid syntax: %s' % yml_error)
            return config
    except FileNotFoundError as e:
        return yaml.safe_load(EMPTY_CONFIG)


def get_cluster_config(cluster, config):
    for c in config['clusters']:
        if c['name'] == cluster:
            return c['cluster']


def get_user_config(user, config):
    for c in config['users']:
        if c['name'] == user:
            return c['user']


def get_context_config(context, config):
    for c in config['contexts']:
        if c['name'] == context:
            return c['context']


def get_current_context(config):
    if 'current-context' in config:
        current_context = config['current-context']
        if not current_context:
            handle_error('current context not available in client configuration')
        context = get_context_config(current_context, config)
        if not context:
            handle_error('context %s not available in client configuration' % current_context)
        user = get_user_config(context['user'], config)
        if not user:
            handle_error('user %s not available in client configuration' % context['user'])
        validate_user_config(user)

        cluster = get_cluster_config(context['cluster'], config)
        if not cluster:
            handle_error('cluster %s not available in client configuration' % context['cluster'])
        validate_cluster_config(cluster)
        context['user'] = user
        context['cluster'] = cluster
        return context
    else:
        handle_error('current context not available in client configuration')


def assert_exists(key, config):
    if not key in config or config[key] is None:
        handle_error('config key %s not present in client configuration:\n %s' % (key, config))


def validate_user_config(user_config):
    assert_exists('api-key', user_config)


def validate_cluster_config(cluster_config):
    if 'host' in cluster_config:
        assert_exists('host', cluster_config)
        assert_exists('ports', cluster_config)
        assert_exists('web', cluster_config['ports'])
        assert_exists('sync', cluster_config['ports'])
        assert_exists('minio-data', cluster_config['ports'])
        assert_exists('minio-output', cluster_config['ports'])
        assert_exists('minio-access-key', cluster_config)
        assert_exists('minio-secret-key', cluster_config)
    else:
        assert_exists('api-server', cluster_config)
        assert_exists('sync-server', cluster_config)
    assert_exists('cluster-id', cluster_config)


def get_client_config():
    config = read_config()
    return get_current_context(config)


def generate_config(api_key, host, cluster_config):
    config = """
current-context: default

contexts:
  - name: default
    context:
      cluster: default
      user: default
      environment: {environment}

clusters:
  - name: default
    cluster:
      cluster-id: {cluster_id}
      host: {host}
      ports:
        web: {web_port}
        sync: {sync_port}
        minio-data: {minio_data_port}
        minio-output: {minio_output_port}
      minio-access-key: {minio_access_key}
      minio-secret-key: {minio_secret_key}

users:
- name: default
  user:
    name: {user_name}
    api-key: {api_key}
""".format(cluster_id=cluster_config.cluster_id,
           host=host,
           web_port=cluster_config.ports.web,
           sync_port=cluster_config.ports.sync,
           minio_data_port=cluster_config.ports.minio_data,
           minio_output_port=cluster_config.ports.minio_output,
           minio_access_key=cluster_config.minio_access_key,
           minio_secret_key=cluster_config.minio_secret_key,
           user_name=cluster_config.user,
           api_key=api_key,
           environment=cluster_config.environment)
    return config


def write_config(api_key, host, cluster_config):
    try:
        os.makedirs(os.path.dirname(get_config_file()))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
    config = generate_config(api_key, host, cluster_config)
    with open(get_config_file(), 'wt') as f:
        f.write(config)


def get_user():
    return get_client_config()['user']['name']

def get_cluster_host():
    return get_client_config()['cluster']['host']


def get_api_server():
    web_port = get_client_config()['cluster'].get('ports', {}).get('web', None)
    if web_port:
        return 'http://' + get_cluster_host() + ':' + str(web_port)
    else:
        # Use old config format
        return get_client_config()['cluster']['api-server']


def get_sync_url():
    sync_port = get_client_config()['cluster'].get('ports', {}).get('sync', None)
    if sync_port:
        return 'rsync://' + get_cluster_host() + ':' + str(sync_port) + '/sync'
    else:
        # Use old config format
        return get_client_config()['cluster']['sync-server']


def get_api_url(api_server=None):
    if not api_server:
        return get_api_server() + '/api'
    else:
        return api_server + '/api'


def get_git_url():
    return get_api_server() + '/git'


def handle_old_config_error():
    handle_error('This new feature requires you to re-login to your cluster first.')


def get_minio_data_host():
    minio_port = get_client_config()['cluster'].get('ports', {}).get('minio-data', None)
    if minio_port:
        return get_cluster_host() + ':' + str(minio_port)
    else:
        handle_old_config_error()


def get_minio_output_host():
    minio_port = get_client_config()['cluster'].get('ports', {}).get('minio-output', None)
    if minio_port:
        return get_cluster_host() + ':' + str(minio_port)
    else:
        handle_old_config_error()


def get_minio_access_key():
    minio_access_key = get_client_config()['cluster'].get('minio-access-key', None)
    if minio_access_key:
        return minio_access_key
    else:
        handle_old_config_error()


def get_minio_secret_key():
    minio_secret_key = get_client_config()['cluster'].get('minio-secret-key', None)
    if minio_secret_key:
        return minio_secret_key
    else:
        handle_old_config_error()


def get_api_key():
    return get_client_config()['user']['api-key']


def get_stream_url():
    api_server = get_api_server()
    return "ws://%s/stream" % urlparse(api_server).netloc


def get_rollbar_endpoint():
    default = 'https://backend.riseml.com/errors/client/'
    if get_environment() == 'staging':
        default = 'https://backend.riseml-staging.com/errors/client/'
    return get_client_config()['cluster'].get('rollbar-server', default)


def get_riseml_url():
    url = 'https://riseml.com/'
    if get_environment() == 'staging':
        url = 'https://riseml-staging.com/'
    return get_client_config().get('backend', url)


def get_cluster_id():
    return get_client_config()['cluster']['cluster-id']


def get_environment():
    return get_client_config().get('environment', 'production')