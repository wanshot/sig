# -*- coding: utf-8 -*-

import os
import sys
import termios
import tty
import codecs
from ansi import term
from terminalsize import get_terminal_size


class SIG(object):

    def __init__(self, output_encodeing, input_encodeing='utf-8'):
        self.pos = 0
        self.width, self.height = get_terminal_size()
        self.output_encodeing = output_encodeing
        self.input_encoding = input_encodeing

    def __enter__(self):
        stream = codecs.getreader(self.input_encoding)(sys.stdin)
        self.lines = map(str, stream)
        self.max_lines_range = len(self.lines)
        ttyname = get_ttyname()
        sys.stdin = file(ttyname)
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
        # hide cursor
        sys.stdout.write('\x1b[?25l')
        for idx, line in enumerate(self.lines):
            line.encode(self.output_encodeing)
            sys.stdout.write('\x1b[0K')
            if idx == self.pos:
                sys.stdout.write(term(line, 'yellow', 'purple', 'bold') + '\r')
            else:
                sys.stdout.write(line + '\x1b[0K' + '\r')
        sys.stdout.write('\x1b[{value}A'.format(value=self.max_lines_range))


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
