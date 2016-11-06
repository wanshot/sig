# -*- coding: utf-8 -*-

import sys
import locale
import argparse
import textwrap

from ansi import term
from core import SIG

LOGAPPNAME = 'WorkFlow Shell Interface'


def get_locale():
    locale.setlocale(locale.LC_ALL, '')
    output_encoding = locale.getpreferredencoding()
    return output_encoding


def get_argparser():
    from sig import __version__, __logo__

    parser = argparse.ArgumentParser(
        usage='sig',
        description=textwrap.dedent(
            term(LOGAPPNAME, fg_color='red') + '\n' +
            term(__logo__, fg_color='red', style='bold')
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-v', '--version',
                        action='version',
                        version='{version}'.format(version=__version__))

    parser.add_argument('command',
                        nargs='?',
                        type=str)

    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()
    if not sys.stdin.isatty():
        encoding = get_locale()
        with SIG(encoding) as sig:
            sig.loop()
    elif args.command is None:
        parser.print_help()
