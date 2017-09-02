#!/usr/bin/env python

from __future__ import absolute_import

import errno
import time
import sys
import os

try:
    from src.abstract.automata.automata import *
    from src.abstract.generator.generator import *
    from src.abstract.parser.parser import *
    from src.abstract.lexer.token import *
    from src.abstract.lexer.lexer import *
    from src.mindslab.generator import *
    from src.mindslab.grammar import *
    from src.mindslab.syntax import *
    from src.debug import *
    import argparse
    import unittest
    import pickle
except ImportError as message:
    raise ImportError(message)

__program__ = 'hmdc'
__version__ = '1.0.0-alpha'
__license__ = 'MIT'


if __name__ == '__main__':

    # adjust path if `this` is packed executable.
    if __package__ is None and not hasattr(sys, 'frozen'):
        path = os.path.realpath(os.path.abspath(__file__))
        sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

    # arguments
    aparser = argparse.ArgumentParser(prog=__program__)
    n_data = aparser.add_argument_group('data arguments')
    n_build = aparser.add_argument_group('build arguments')
    n_optim = aparser.add_argument_group('optimization arguments')
    n_test = aparser.add_argument_group('testing arguments')

    # -v, --version: show program's version number and exit.
    aparser.add_argument('-v', '--version',
                         action='version',
                         version=__version__)

    #
    # test
    #

    # -t: run test suite and exit.
    n_test.add_argument('-t', '--test',
                        action='store_true',
                        default=False,
                        help="run tests (default: off)")

    #
    # data
    #

    # -f <file>: compile file hmd definition.
    n_data.add_argument('-f',
                        type=str,
                        nargs='?',
                        metavar='file',
                        help='compile file (default: output to STDOUT)')

    # -c <str>: compile single inline (hmd) definition.
    n_data.add_argument('-c',
                        type=str,
                        nargs='?',
                        metavar='str',
                        help='compile string (default: output to STDOUT)')

    # -o <file>: output matrix into file.
    n_data.add_argument('-o',
                        type=str,
                        nargs='?',
                        default='output.matrix',
                        metavar='file',
                        help="save output to file (default: 'result.matrix')")

    #
    # build
    #

    # -l <int>: limit total categories count. Any defincies or extraneous
    #           categories will automatically repair itself.
    #
    # [example]
    # - case #1: limit = 3
    #   A  B  C  {definition} => A  B  C  {definition}
    #   D  E  F  {definition} => D  E  F  {definition}
    # - case #2: limit = 2
    #   A  B  C     {definition} => A  B  C    {definition}
    #   D  E  F  G  {definition} => D  E  F_G  {definition}
    # - case #3: limit = 4
    #   A  B  C  D  {definition} => A  B  C  D   {definition}
    #   E  F  G     {definition} => E  F  G  \t  {definition}
    n_build.add_argument('-l',
                         type=int,
                         nargs='?',
                         default=10,
                         metavar='int',
                         help='set limit to category count (default: 10)')

    # -Og: optimize ouptut matrix definitions by sorting the groupings.
    #
    # [example]
    # - case #1: (c|b|a)(a|b)(d|c|x) => (a|b|c)(a|b)(c|d|x)
    # - case #2: (c|b|a)(@b|@a)(d|c|x) => (a|b|c)(@b|@a)(c|d|x)
    # - case #3: (c|b|a)(+1b|+2a)(d|c|x) => (a|b|c)(+1b|+2a)(c|d|x)
    # - case #4: (c|b|a)(+1b|a)(d|c|x) => (a|b|c)(a|+1b)(c|d|x)
    n_optim.add_argument('-Og',
                         action='store_true',
                         default=False,
                         help='sort inline definition groups (default: off)')

    # parse arguments
    args = aparser.parse_args()

    if args.test:

        # override non-test output to /dev/null
        null = open(os.devnull, 'wb')
        sys.stdout = sys.stderr = null

        test_suites, test_cases = [], (
            # TestLexer,
            # TestParserEnglish
        )

        for test_case in test_cases:
            test_suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
            test_suites.append(test_suite)

        # run tests
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(test_suites))
        sys.exit(not result.wasSuccessful())

    else:
        generator = HMDGenerator()

        # compile file
        if args.f:
            filename = args.f
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    c = f.read().split('\n')
                    f.close()
                sys.stdout.write(generator.generate(c))
            else:
                debug('w', "file '%s' does not exist.\n" % filename)
                sys.exit(1)

        # compile string
        if args.c:
            sys.stdout.write(generator.generate(args.c))
