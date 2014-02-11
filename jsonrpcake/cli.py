"""CLI arguments definition.

NOTE: the CLI interface may change before reaching v1.0.

"""
from . import __doc__
from textwrap import dedent, wrap
#noinspection PyCompatibility
from argparse import (RawDescriptionHelpFormatter, FileType,
                      ZERO_OR_MORE, SUPPRESS)

from . import __version__
from .output import AVAILABLE_STYLES, DEFAULT_STYLE
from .input import (Parser, KeyValueArgType,
                    SEP_GROUP_ALL_ITEMS,
                    PRETTY_MAP, PRETTY_STDOUT_TTY_ONLY)


class JSONRPCakeHelpFormatter(RawDescriptionHelpFormatter):
    """A nicer help formatter.

    Help for arguments can be indented and contain new lines.
    It will be de-dented and arguments in the help
    will be separated by a blank line for better readability.


    """
    def __init__(self, max_help_position=6, *args, **kwargs):
        # A smaller indent for args help.
        kwargs['max_help_position'] = max_help_position
        super(JSONRPCakeHelpFormatter, self).__init__(*args, **kwargs)

    def _split_lines(self, text, width):
        text = dedent(text).strip() + '\n\n'
        return text.splitlines()

parser = Parser(
    formatter_class=JSONRPCakeHelpFormatter,
    description=__doc__,
    epilog=dedent("""
    For every --OPTION there is also a --no-OPTION that reverts OPTION
    to its default value.
    """)
)


#######################################################################
# Positional arguments.
#######################################################################

positional = parser.add_argument_group(
    title='Positional arguments',
    description=dedent("""
    These arguments come after any flags and in the order they are listed here.

    """)
)

positional.add_argument(
    'addr',
    metavar='ADDR',
    help="""
    You can also use a shorthand for localhost

        $ jsonrpc :3000 METHOD     # => jsonrpc localhost:3000 METHOD

    """
)

positional.add_argument(
    'method',
    metavar='METHOD',
    default=None,
    help="The JSONRPC method to be used for the request."
)

positional.add_argument(
    'items',
    metavar='REQUEST_ITEM',
    nargs=ZERO_OR_MORE,
    type=KeyValueArgType(*SEP_GROUP_ALL_ITEMS),
    help=r"""
    Optional key-value pairs to be included in the request. The separator used
    determines the type:

    '=' Data fields to be serialized into a JSON object:

        name=JSONRPCake  language=Python  description='CLI JSONRPC client'

    ':=' Non-string JSON data fields:

        awesome:=true  amount:=42  colors:='["red", "green", "blue"]'

    ':=@' A raw JSON field like ':=', but takes a file path and embeds its
    content:

        package:=@./package.json

    You can use a backslash to escape a colliding separator in the field name:

        field-name-with\:colon=value

    """
)


#######################################################################
# Output processing
#######################################################################

output_processing = parser.add_argument_group(title='Output processing')

output_processing.add_argument(
    '--pretty',
    dest='prettify',
    default=PRETTY_STDOUT_TTY_ONLY,
    choices=sorted(PRETTY_MAP.keys()),
    help="""
    Controls output processing. The value can be "none" to not prettify
    the output (default for redirected output), "all" to apply both colors
    and formatting (default for terminal output), "colors", or "format".

    """
)
output_processing.add_argument(
    '--style', '-s',
    dest='style',
    metavar='STYLE',
    default=DEFAULT_STYLE,
    choices=AVAILABLE_STYLES,
    help="""
    Output coloring style (default is "{default}"). One of:

{available}

    For this option to work properly, please make sure that the $TERM
    environment variable is set to "xterm-256color" or similar
    (e.g., via `export TERM=xterm-256color' in your ~/.bashrc).

    """
    .format(
        default=DEFAULT_STYLE,
        available='\n'.join(
            '{0: >20}'.format(line.strip())
            for line in
            wrap(' '.join(sorted(AVAILABLE_STYLES)), 60)
        ),
    )
)


#######################################################################
# Output options
#######################################################################
output_options = parser.add_argument_group(title='Output options')

#output_options.add_argument(
#    '--verbose', '-v',
#    dest='output_options',
#    action='store_const',
#    const=''.join(OUTPUT_OPTIONS),
#    help="""
#    Print the whole request as well as the response. Shortcut for --print={0}.
#
#    """
#    .format(''.join(OUTPUT_OPTIONS))
#)
output_options.add_argument(
    '--output', '-o',
    type=FileType('a+b'),
    dest='output_file',
    metavar='FILE',
    help="""
    Save output to FILE. If --download is set, then only the response body is
    saved to the file. Other parts of the HTTP exchange are printed to stderr.

    """

)


#######################################################################
# Network
#######################################################################

network = parser.add_argument_group(title='Network')

network.add_argument(
    '--timeout',
    type=float,
    default=30,
    metavar='SECONDS',
    help="""
    The connection timeout of the request in seconds. The default value is
    30 seconds.

    """
)
network.add_argument(
    '--check-status',
    default=False,
    action='store_true',
    help="""
    By default, JSONRPCake exits with 0 when no network or other fatal errors
    occur. This flag instructs JSONRPCake to also check the JSON-RPC response
    exit with an error if the response indicates one.
    """
)


#######################################################################
# Troubleshooting
#######################################################################

troubleshooting = parser.add_argument_group(title='Troubleshooting')

troubleshooting.add_argument(
    '--ignore-stdin',
    action='store_true',
    default=False,
    help="""
    Do not attempt to read stdin.

    """
)
troubleshooting.add_argument(
    '--help',
    action='help',
    default=SUPPRESS,
    help="""
    Show this help message and exit.

    """
)
troubleshooting.add_argument(
    '--version',
    action='version',
    version=__version__,
    help="""
    Show version and exit.

    """
)
troubleshooting.add_argument(
    '--traceback',
    action='store_true',
    default=False,
    help="""
    Prints exception traceback should one occur.

    """
)
troubleshooting.add_argument(
    '--debug',
    action='store_true',
    default=False,
    help="""
    Prints exception traceback should one occur, and also other information
    that is useful for debugging JSONRPCake itself and for reporting bugs.

    """
)
