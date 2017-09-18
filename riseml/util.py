# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import time
import re
import platform

from datetime import datetime

from riseml.consts import IS_BUNDLE, ENDPOINT_URL

USER_ONLY_REGEX = re.compile(r'^\.[^\.]+$')
EXPERIMENT_ID_REGEX = re.compile(r'^(\.[^\.]+\.)?\d+(\.\d+)?$')
JOB_ID_REGEX = re.compile(r'^(\.[^\.]+\.)?\d+(\.\d+)?\.[A-Za-z]+(\.\d+)?$')

class JobState(object):

    created  = 'CREATED'
    building = 'BUILDING'
    pending  = 'PENDING'
    starting = 'STARTING'
    pausing  = 'PAUSING'
    running  = 'RUNNING'
    serving  = 'SERVING'
    failed   = 'FAILED'
    finished = 'FINISHED'
    killed   = 'KILLED'


COLOR_CODES = {
    # 'black': 30,     NOTE: We don't want that color!
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'light gray': 37,
    'dark gray': 90,
    'light red': 91,
    'light green': 92,
    'light yellow': 93,
    'light blue': 94,
    'light magenta': 95,
    'light cyan': 96,
    'white': 97
}

colors = {}

COLORS_DISABLED = not sys.stdout.isatty()

def bold(s): return color_string(s, ansi_code=1)

def get_color_pairs():
    for name, code in COLOR_CODES.items():
        yield(name, str(code))
        yield('bold_' + name, str(code) + ';1')


for (name, ansi_code) in get_color_pairs():
    colors[name] = ansi_code


def ansi_sequence(code):
    return "\033[%sm" % code


def color_string(s, color=None, ansi_code=None):
    assert color is not None or ansi_code is not None, "You need to supply `color` or `ansi_code` param."
    assert not (color is not None and ansi_code is not None), "You need to supply either `color` or `ansi_code`"

    if COLORS_DISABLED:
        # return non-colored string if non-terminal output
        return s
    else:
        if color:
            ansi_code = colors[color]
        return "%s%s%s" % (ansi_sequence(ansi_code), s, ansi_sequence(0))


class TableElement():
    pass

class TableRowDelimiter(TableElement):
    def __init__(self, symbol):
        self.symbol = symbol
    def __str__(self):
        return 'TableRowDelimiter ({})'.format(self.symbol)


def print_table(header, rows, min_widths=None, 
                file=sys.stdout, separator=False, bold_header=True,
                col_separator_spaces=1):
      
    n_columns = len(header)

    if not min_widths:
        widths = [5] * n_columns  # 5 is default width
    else:
        widths = list(min_widths)
    
    for i, (h, w) in enumerate(zip(header, widths)):
        if len(h) > w:
            widths[i] = len(h)

    for row in rows:
        # skip table elements as non-data rows
        if isinstance(row, TableElement):
           continue

        row_items_count = len(row)
        assert row_items_count == n_columns, \
            "Column %s (columns: %d) must match" \
            " header's colums count: %d" % (str(row), row_items_count, n_columns)

        for i, cell in enumerate(row):
            item_len = len(cell) if not isinstance(cell, int) else len(str(cell))

            if item_len > widths[i]:
                widths[i] = item_len

    table_width = sum(widths) + n_columns - 1

    # see https://pyformat.info/
    # `Padding and aligning strings` block
    line_pattern = ''.join([
        u'{:%s{widths[%s]}}%s' % ('<', i, ' ' * col_separator_spaces)
        for i in range(n_columns)
    ])

    def render_line(columns): return line_pattern.format(*columns, widths=widths)

    # print separator
    if separator:
        print('-' * len(render_line(header)), file=file)

    # print header
    if not bold_header:
        emph = lambda x: x
    else:
        emph = bold
    print(emph(render_line(header)), file=file)

    # print rows
    for row in rows:
        if isinstance(row, TableRowDelimiter):
            print(row.symbol * table_width, file=file)
        else:
            print(render_line(row), file=file)


def get_since_str(timestamp):
    if not timestamp:
        return '-'
    now = int(time.time() * 1000)
    since_ms = now - timestamp
    days, since_ms = divmod(since_ms, 24 * 60 * 60 * 1000)
    hours, since_ms = divmod(since_ms, 60 * 60 * 1000)
    minutes, since_ms = divmod(since_ms, 60 * 1000)
    seconds, since_ms = divmod(since_ms, 1000)
    if days > 0:
        return "%s day(s)" % days
    elif hours > 0:
        return "%s hour(s)" % hours
    elif minutes > 0:
        return "%s minute(s)" % minutes
    elif seconds > 0:
        return "%s second(s)" % seconds
    else:
        return "just now"


def str_timestamp(timestamp):
    return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%dT%H:%M:%SZ')


def mib_to_gib(value):
    return float(value) * (10 ** 6) / (1024 ** 3)


def bytes_to_gib(value):
    return float(value) / (1024 ** 3)


def bytes_to_mib(value):
    return float(value) / (1024 ** 2)


def bytes_to_kib(value):
    return float(value) / (1024 ** 1)


def get_readable_size(value):
    for f, u in ((bytes_to_gib, 'GB'), (bytes_to_mib, 'MB') , 
                 (bytes_to_kib, 'KB')):
        if f(value) >= 1:
            return '%.1f %s' % (f(value), u)
    return '%s B' % (value)


def get_rsync_path():
    if IS_BUNDLE:
        return os.path.join(sys._MEIPASS, 'bin', 'rsync')
    else:
        return resolve_path('rsync')


def resolve_path(binary):
    paths = os.environ.get('PATH', '').split(os.pathsep)
    exts = ['']
    if platform.system() == 'Windows':
        path_exts = os.environ.get('PATHEXT', '.exe;.bat;.cmd').split(';')
        has_ext = os.path.splitext(binary)[1] in path_exts
        if not has_ext:
            exts = path_exts
    for path in paths:
        for ext in exts:
            loc = os.path.join(path, binary + ext)
            if os.path.isfile(loc):
                return loc


from riseml.client.rest import ApiException
from riseml.errors import handle_http_error, handle_error
from urllib3.exceptions import HTTPError


def call_api(api_fn, not_found=None):
    try:
        return api_fn()
    except ApiException as e:
        if e.status == 0:
            raise e
        elif e.status == 401:
            handle_error("You are not authorized!")
        elif e.status == 404 and not_found:
            not_found()
        else:
            handle_http_error(e.body, e.status)
    except HTTPError as e:
        handle_error('Could not connect to API ({host}:{port}{url}) — {exc_type}'.format(
            host=e.pool.host,
            port=e.pool.port,
            url=e.url,
            exc_type=e.__class__.__name__
        ))

def is_job_id(id):
    return JOB_ID_REGEX.match(id) is not None

def is_experiment_id(id):
    return EXPERIMENT_ID_REGEX.match(id) is not None

def is_user_id(id):
    return USER_ONLY_REGEX.match(id) is not None

def has_tensorboard(experiment):
    return experiment.framework == 'tensorflow' and \
        experiment.framework_config.get('tensorboard', False)

def is_tensorboard_job(job):
    return job.role == 'tensorboard'

def tensorboard_job(experiment):
    return next((job for job in experiment.jobs if is_tensorboard_job(job)), None)

def tensorboard_job_url(job):
    return "{}/{}".format(ENDPOINT_URL, job.service_name)
