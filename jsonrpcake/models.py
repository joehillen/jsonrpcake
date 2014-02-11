import os
import sys

from .compat import is_windows


class Environment(object):
    """Holds information about the execution context.

    Groups various aspects of the environment in a changeable object
    and allows for mocking.

    """

    is_windows = is_windows

    progname = os.path.basename(sys.argv[0])
    if progname != 'jsonrpc':
        progname = 'jsonrpc'

    # Can be set to 0 to disable colors completely.
    colors = 256 if '256color' in os.environ.get('TERM', '') else 88

    stdin = sys.stdin
    stdin_isatty = sys.stdin.isatty()

    stdout_isatty = sys.stdout.isatty()
    stderr_isatty = sys.stderr.isatty()
    if is_windows:
        # noinspection PyUnresolvedReferences
        from colorama.initialise import wrap_stream
        stdout = wrap_stream(sys.stdout, convert=None,
                             strip=None, autoreset=True, wrap=True)
        stderr = wrap_stream(sys.stderr, convert=None,
                             strip=None, autoreset=True, wrap=True)
    else:
        stdout = sys.stdout
        stderr = sys.stderr

    def __init__(self, **kwargs):
        assert all(hasattr(type(self), attr)
                   for attr in kwargs.keys())
        self.__dict__.update(**kwargs)
