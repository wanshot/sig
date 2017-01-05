# -*- coding: utf-8 -*-

import os
import sys
import locale
import argparse
import textwrap

from ansi import term
from core import SIG

LOGAPPNAME = 'Selection Display Interface'


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

    parser.add_argument('filename',
                        nargs='?',
                        type=str)

    parser.add_argument('-s', '--search',
                        nargs='?',
                        type=str)

    parser.add_argument('-e', '--execute',
                        nargs='?',
                        type=str)

    parser.add_argument('-c', '--into_clipboald',
                        nargs='?',
                        type=str)

    parser.add_argument('-r', '--regex',
                        nargs='?',
                        type=str)

    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()
    if args.filename and not os.access(args.filename, os.R_OK):
        sys.exit('Not read a file')
#     if sys.stdin.isatty():
#         sys.exit('Not a tty file')
    encoding = get_locale()
    with SIG(encoding, filename=args.filename) as sig:
        sig.loop()
