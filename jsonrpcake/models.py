import os
import sys


class Environment(object):
    """Holds information about the execution context.

    Groups various aspects of the environment in a changeable object
    and allows for mocking.

    """

    progname = os.path.basename(sys.argv[0])
    if progname != 'jsonrpc':
        progname = 'jsonrpc'

    # Can be set to 0 to disable colors completely.
    colors = 256 if '256color' in os.environ.get('TERM', '') else 88

    stdin = sys.stdin
    stdin_isatty = sys.stdin.isatty()

    stdout_isatty = sys.stdout.isatty()
    stderr_isatty = sys.stderr.isatty()
    stdout = sys.stdout
    stderr = sys.stderr

    def __init__(self, **kwargs):
        assert all(hasattr(type(self), attr)
                   for attr in kwargs.keys())
        self.__dict__.update(**kwargs)
