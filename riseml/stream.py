from __future__ import print_function

import re
import json
import sys
import websocket
import stringcase

from riseml.errors import handle_error
from riseml.client_config import get_stream_url
from riseml.ansi import COLOR_CODES, color_string
from . import util

ANSI_ESCAPE_REGEX = re.compile(r'\x1b\[(\d+)m')
TENSORBOARD_STARTING_REGEX = re.compile(r'(TensorBoard ([^\s]+) at )(http://[^:]+:\d+[^\s]*)')
HOROVOD_LOG_REGEX = re.compile(r'\[1,(\d+)\]<(stderr|stdout)>:')
HOROVOD_WORKER_REGEX = re.compile(r'worker\.\d+')

class LogPrinter(object):
    def __init__(self, url, ids_to_name, stream_meta=None):
        self.url = url
        self.ids_to_name = ids_to_name
        self.stream_meta = stream_meta or {}

        self.job_ids_color = {
            id: list(COLOR_CODES.keys())[(i + 1) % len(COLOR_CODES)]
            for i, id in enumerate(list(self.ids_to_name.keys()))
        }

        self.job_ids_last_color_used = {}
        self.indentation = max([len(name) for _, name in self.ids_to_name.items()]) + 1

    def stream(self):
        ws_app = websocket.WebSocketApp(
            self.url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        # FIXME: {'Authorization': os.environ.get('RISEML_APIKEY')}
        ws_app.run_forever()

    def _on_message(self, _, message):
        msg = json.loads(message)
        msg_type = msg['type']

        if msg_type == 'log':
            self.print_log_message(msg)
        elif msg_type == 'state':
            self.print_state_message(msg)
        elif msg_type == 'error':
            self.print_error_message(msg)

    def _on_error(self, _, error):
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            any_id = self.stream_meta.get('experiment_id') or self.stream_meta.get('job_id')
            print()  # newline after ^C
            if self.stream_meta.get('experiment_id'):
                print('Experiment will continue in background')
            else:
                print('Job will continue in background')
            if any_id:
                print('Type `riseml logs %s` to connect to log stream again' % any_id)
        else:
            # all other Exception based stuff goes to `handle_error`
            handle_error(error)

    def _on_close(self, _):
        sys.exit(0)

    def _message_prefix(self, msg):
        job_name = self.ids_to_name[msg['job_id']]
        if 'name_suffix' in msg:
            job_name += msg['name_suffix']
        color = self.job_ids_color[msg['job_id']]
        prefix = "{}| ".format(job_name.ljust(self.indentation))

        return color_string(prefix, color=color)
    
    def _apply_horovod_mapping(self, msg):
        if HOROVOD_LOG_REGEX.match(msg['line']):
            processes_per_worker = self.stream_meta.get("horovod_processes")
            matches = HOROVOD_LOG_REGEX.findall(msg['line'])
            process_id = int(matches[0][0])
            worker_name = re.sub(HOROVOD_WORKER_REGEX,
                                 'worker.{}'.format(process_id // processes_per_worker + 1),
                                 self.ids_to_name[msg['job_id']])
            for item in self.ids_to_name.items():
                if item[1] == worker_name:
                    msg['job_id'] = item[0]
            msg['line'] = re.sub(HOROVOD_LOG_REGEX, '', msg['line'])
            if processes_per_worker > 1:
                msg['name_suffix'] = '.{}'.format(process_id % processes_per_worker + 1)

    def print_log_message(self, msg):
        if msg['job_id'] not in self.ids_to_name:
            return
        self._apply_horovod_mapping(msg)
        if self.stream_meta.get('filter_job', False) and msg['job_id'] != self.stream_meta['filter_job'].id:
            return
        line = msg['line']
        if 'tensorboard' in self.ids_to_name[msg['job_id']] \
            and self.stream_meta.get("tensorboard_job"):
            line = re.sub(TENSORBOARD_STARTING_REGEX,
                            r'\1{}'.format(
                                util.tensorboard_job_url(self.stream_meta.get("tensorboard_job"))
                            ),
                            line)
        for partial_line in line.split('\r'):
            last_color = self.job_ids_last_color_used.get(msg['job_id'], 0)
            line_text = "[%s] %s" % (util.str_timestamp(msg['time']),
                                    color_string(partial_line, ansi_code=last_color))

            output = "%s%s" % (self._message_prefix(msg), line_text)
            sys.stdout.write(output)
            sys.stdout.write('\r')

            used_colors = ANSI_ESCAPE_REGEX.findall(partial_line)
            if used_colors:
                self.job_ids_last_color_used[msg['job_id']] = used_colors[-1]
        sys.stdout.write('\n')

    def print_state_message(self, msg):
        if msg['job_id'] not in self.ids_to_name:
            return
        if self.stream_meta.get('filter_job', False) and msg['job_id'] != self.stream_meta['filter_job'].id:
            return
        time = util.str_timestamp(msg['time'])
        state = "[%s] --> %s" % (time, msg['state'])
        output = "%s%s" % (self._message_prefix(msg),
                           color_string(state, color="bold_white"))
        print(output)
        for key in ['reason', 'message', 'exit_code']:
            if msg.get(key, None) is not None:
                message = "[{}] {}: {}".format(time, stringcase.titlecase(key), msg[key])
                print("{}{}".format(self._message_prefix(msg), color_string(message, color="bold_white")))

    def print_error_message(self, msg):
        print(color_string("Error: {}".format(msg['error']), color="red"))

def stream_job_log(job):
    ids_to_name = {job.id: job.short_id}
    url = '%s/ws/jobs/%s/stream' % (get_stream_url(), job.id)
    meta = {"job_id": job.short_id}
    if util.is_tensorboard_job(job):
        meta["tensorboard_job"] = job
    LogPrinter(url, ids_to_name, stream_meta=meta).stream()


def stream_experiment_log(experiment, filter_job=None):
    def add_experiment_to_log(experiment):
        ids_to_name[experiment.id] = experiment.short_id
        for job in experiment.jobs:
            ids_to_name[job.id] = '{}.{}'.format(experiment.short_id, job.name)

    url = '%s/ws/experiments/%s/stream' % (get_stream_url(), experiment.id)
    ids_to_name = {}
    jobs = experiment.jobs
    add_experiment_to_log(experiment)
    for child_experiment in experiment.children:
        jobs += child_experiment.jobs
        add_experiment_to_log(child_experiment)

    horovod_gpus = max([job.gpus for job in jobs if job.role == 'tf-hrvd-master'] + [0])
    horovod_processes = experiment.framework_config or {}
    horovod_processes = horovod_processes.get('horovod', {}) or {}
    horovod_processes = horovod_processes.get('workers', {}) or {}
    horovod_processes = horovod_processes.get('processes', None)
    meta = {
        "experiment_id": experiment.short_id,
        "filter_job": filter_job,
        "horovod_processes":  horovod_processes or horovod_gpus or 1
    }
    if util.has_tensorboard(experiment):
        meta["tensorboard_job"] = util.tensorboard_job(experiment)
    LogPrinter(url, ids_to_name, stream_meta=meta).stream()
