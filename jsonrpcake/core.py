"""This module provides the main functionality of JSONRPCake.

Invocation flow:

    1. Read, validate and process the input (args, `stdin`).
    2. Create and send a request.
    3. Stream, and possibly process and format, the requested parts
       of the request-response exchange.
    4. Simultaneously write to `stdout`
    5. Exit.

"""
import sys
import errno
import json

import jsonrpc_ns

from .models import Environment
from .output import build_output_stream, write, write_with_colors_win_py3
from . import ExitStatus


def main(args=sys.argv[1:], env=Environment()):
    """Run the main program and write the output to ``env.stdout``.

    Return exit status code.

    """
    from .cli import parser

    def error(msg, *args, **kwargs):
        msg = msg % args
        level = kwargs.get('level', 'error')
        env.stderr.write('\njsonrpc: {level}: {msg}\n'.format(level=level,
                                                              msg=msg))

    debug = '--debug' in args
    traceback = debug or '--traceback' in args
    exit_status = ExitStatus.OK

    if debug:
        if args == ['--debug']:
            return exit_status

    try:
        args = parser.parse_args(args=args, env=env)
        try:
            response = jsonrpc_ns.request(args.addr, args.method, args.data)
        except jsonrpc_ns.JSONRPCResponseError as e:
            response = e.value
            code = e.value['code']
            message = e.value['message']

            if args.check_status:
                exit_status = ExitStatus.ERROR
                error('JSONRPC %s %s', code, message, level='warning')

        response = json.dumps(response)

        write_kwargs = {
            'stream': build_output_stream(
                args, env, None, response),

            'outfile': env.stdout,

            'flush': env.stdout_isatty or args.stream
        }

        try:
            write(**write_kwargs)

        except IOError as e:
            if not traceback and e.errno == errno.EPIPE:
                # Ignore broken pipes unless --traceback.
                env.stderr.write('\n')
            else:
                raise
    except (KeyboardInterrupt, SystemExit):
        if traceback:
            raise
        env.stderr.write('\n')
        exit_status = ExitStatus.ERROR

    except Exception as e:
        # TODO: Better distinction between expected and unexpected errors.
        #       Network errors vs. bugs, etc.
        if traceback:
            raise
        error('%s: %s', type(e).__name__, str(e))
        exit_status = ExitStatus.ERROR

    return exit_status
