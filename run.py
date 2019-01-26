import argparse
import pickle
import socket

from yourmodule import config
from yourmodule.jobs import your_job, backup_job

hostname = socket.gethostname()


def run_on_cluster():
    """
    run multiple jobs on multiple LudwigCluster nodes.
    """
    config.Dirs.corpora = config.Dirs.remote_root / 'corpora'
    config.Dirs.tasks = config.Dirs.remote_root / 'tasks'
    #
    p = config.Dirs.remote_root / '{}_param2val_chunk.pkl'.format(hostname)
    with p.open('rb') as f:
        param2val_chunk = pickle.load(f)
    for param2val in param2val_chunk:
        your_job(param2val)
        backup_job(param2val['param_name'], param2val['job_name'], allow_rewrite=False)
    #
    print('Finished all jobs.')
    print()


def run_on_host():
    """
    run jobs on the local host for testing/development
    """


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', default=False, action='store_true', dest='local', required=False)
    namespace = parser.parse_args()
    if namespace.local:
        run_on_host()
    else:
        run_on_cluster()