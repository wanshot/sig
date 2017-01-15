# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import termios
import tty
import codecs

from .ansi import term
from .terminalsize import get_terminal_size


class SIG(object):

    def __init__(self, output_encodeing, filename=None, input_encodeing='utf-8'):
        self.pos = 0
        self.filename = filename
        self.width, self.height = get_terminal_size()
        self.output_encodeing = output_encodeing
        self.input_encoding = input_encodeing

    def __enter__(self):
        if self.filename:
            stream = codecs.getreader(self.input_encoding)(open(self.filename, 'rb'), 'replace')
        else:
            stream = codecs.getreader(self.input_encoding)(sys.stdin.buffer)
        self.lines = stream.readlines()
        self.max_lines_range = len(self.lines)
        ttyname = get_ttyname()
        sys.stdin = open(ttyname)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write('\x1b[?25h')

    def loop(self):
        self.render()
        try:
            while True:

                ch = get_char()
                if ch == 'q':
                    sys.exit(1)
                # Enter
                elif ch == '\r':
                    sys.exit(1)
                # CURSOR KEY
                elif ch == '\x1b':
                    sys.exit(1)
                elif ch == 'k':
                    if self.pos > 0:
                        self.pos -= 1
                elif ch == 'j':
                    if self.pos < self.max_lines_range - 1:
                        self.pos += 1

                if ch:
                    self.render()
        except:
            sys.stdout.write('\x1b[?0h\x1b[0J')

    def render(self):
        reset = '\x1b[0K\x1b[0m'
        sys.stdout.write('\x1b[?25l')  # hide cursor
        for idx, line in enumerate(self.lines):
            line.encode(self.output_encodeing)
            sys.stdout.write('\x1b[0K')
            if idx == self.pos:
                sys.stdout.write(term(line,
                                      'yellow',
                                      'purple',
                                      'bold') + reset + '\r')
            else:
                sys.stdout.write(line + reset + '\r')
        sys.stdout.write('\x1b[{}A'.format(self.max_lines_range))


def get_ttyname():
    for file_obj in (sys.stdin, sys.stdout, sys.stderr):
        if file_obj.isatty():
            return os.ttyname(file_obj.fileno())


def get_char():
    try:
        from msvcrt import getch
        return getch()
    except ImportError:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
