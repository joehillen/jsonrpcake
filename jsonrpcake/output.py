"""Output streaming, processing and formatting.

"""
import json
from itertools import chain

import pygments
from pygments.lexers.web import JsonLexer
from pygments.styles import get_style_by_name, STYLE_MAP
from pygments.formatters.terminal import TerminalFormatter
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.util import ClassNotFound

from .compat import is_windows
from .solarized import Solarized256Style
from .models import Environment


# The default number of spaces to indent when pretty printing
DEFAULT_INDENT = 4

# Colors on Windows via colorama don't look that
# great and fruity seems to give the best result there.
AVAILABLE_STYLES = set(STYLE_MAP.keys())
AVAILABLE_STYLES.add('solarized')
DEFAULT_STYLE = 'solarized' if not is_windows else 'fruity'


BINARY_SUPPRESSED_NOTICE = (
    b'\n'
    b'+-----------------------------------------+\n'
    b'| NOTE: binary data not shown in terminal |\n'
    b'+-----------------------------------------+'
)


class BinarySuppressedError(Exception):
    """An error indicating that the body is binary and won't be written,
     e.g., for terminal output)."""

    message = BINARY_SUPPRESSED_NOTICE


###############################################################################
# Output Streams
###############################################################################


def write(stream, outfile, flush):
    """Write the output stream."""
    try:
        # Writing bytes so we use the buffer interface (Python 3).
        buf = outfile.buffer
    except AttributeError:
        buf = outfile

    for chunk in stream:
        buf.write(chunk)
        if flush:
            outfile.flush()


def write_with_colors_win_py3(stream, outfile, flush):
    """Like `write`, but colorized chunks are written as text
    directly to `outfile` to ensure it gets processed by colorama.
    Applies only to Windows with Python 3 and colorized terminal output.

    """
    color = b'\x1b['
    encoding = outfile.encoding
    for chunk in stream:
        if color in chunk:
            outfile.write(chunk.decode(encoding))
        else:
            outfile.buffer.write(chunk)
        if flush:
            outfile.flush()


def build_output_stream(args, env, request, response):
    """Build and return a chain of iterators over the `request`-`response`
    exchange each of which yields `bytes` chunks.

    """

    req = False
    resp = True

    output = []
    processor = OutputProcessor(
        env=env, groups=args.prettify, pygments_style=args.style)

    if req:
        output.append(processor.process_body(request))
    if req and resp:
        # Request/Response separator.
        output.append([b'\n\n'])

    if resp:
        output.append(processor.process_body(response))

    if env.stdout_isatty and resp:
        # Ensure a blank line after the response body.
        # For terminal output only.
        output.append([b'\n\n'])

    return chain(*output)


###############################################################################
# Processing
###############################################################################

class BaseProcessor(object):
    """Base, noop output processor class."""

    enabled = True

    def __init__(self, env=Environment(), **kwargs):
        """
        :param env: an class:`Environment` instance
        :param kwargs: additional keyword argument that some
                       processor might require.

        """
        self.env = env
        self.kwargs = kwargs

    def process_headers(self, headers):
        """Return processed `headers`

        :param headers: The headers as text.

        """
        return headers

    def process_body(self, content):
        """Return processed `content`.

        :param content: The body content as text
        :param content_type: Full content type, e.g., 'application/atom+xml'.
        :param subtype: E.g. 'xml'.
        :param encoding: The original content encoding.

        """
        return content


class JSONProcessor(BaseProcessor):
    """JSON body processor."""

    def process_body(self, content):
        try:
            # Indent the JSON data, sort keys by name, and
            # avoid unicode escapes to improve readability.
            content = json.dumps(json.loads(content),
                                 sort_keys=True,
                                 ensure_ascii=False,
                                 indent=DEFAULT_INDENT)
        except ValueError:
            # Invalid JSON but we don't care.
            pass
        return content


class PygmentsProcessor(BaseProcessor):
    """A processor that applies syntax-highlighting using Pygments
    to the headers, and to the body as well if its content type is recognized.

    """
    def __init__(self, *args, **kwargs):
        super(PygmentsProcessor, self).__init__(*args, **kwargs)

        # Cache that speeds up when we process streamed body by line.
        if not self.env.colors:
            self.enabled = False
            return

        try:
            style = get_style_by_name(
                self.kwargs.get('pygments_style', DEFAULT_STYLE))
        except ClassNotFound:
            style = Solarized256Style

        if self.env.is_windows or self.env.colors == 256:
            fmt_class = Terminal256Formatter
        else:
            fmt_class = TerminalFormatter
        self.formatter = fmt_class(style=style)

    #def process_headers(self, headers):
    #    return pygments.highlight(
    #        headers, JSONRPCLexer(), self.formatter).strip()

    def process_body(self, content):
        return pygments.highlight(content, JsonLexer(), self.formatter).strip()


class OutputProcessor(object):
    """A delegate class that invokes the actual processors."""

    installed_processors = {
        'format': [
            JSONProcessor
        ],
        'colors': [
            PygmentsProcessor
        ]
    }

    def __init__(self, groups, env=Environment(), **kwargs):
        """
        :param env: a :class:`models.Environment` instance
        :param groups: the groups of processors to be applied
        :param kwargs: additional keyword arguments for processors

        """
        self.processors = []
        for group in groups:
            for cls in self.installed_processors[group]:
                processor = cls(env, **kwargs)
                if processor.enabled:
                    self.processors.append(processor)

    def process_body(self, content):
        for processor in self.processors:
            content = processor.process_body(content)

        return content
