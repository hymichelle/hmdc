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
    from src.mindslab.grammar import *
    from src.mindslab.syntax import *
    from src.debug import *
    import argparse
    import unittest
    import pickle
except ImportError as message:
    raise ImportError(message)


if __name__ == '__main__':

    # adjust path if packed executable
    if __package__ is None and not hasattr(sys, 'frozen'):
        path = os.path.realpath(os.path.abspath(__file__))
        sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

    #
    # arguments
    #

    aparser = argparse.ArgumentParser()

    # -t: run test suite.
    aparser.add_argument('-t',
                         '--test',
                         action='store_true',
                         default=False,
                         help='run test suite.')

    # -O: ouput optimization.
    aparser.add_argument('-O',
                         '--optimize',
                         action='store_true',
                         default=False,
                         help='optimize')

    # parse arguments
    args = aparser.parse_args()

    if args.test:

        # override non-test output to /dev/null
        null = open(os.devnull, 'wb')
        sys.stdout = sys.stderr = null

        test_suites, test_cases = [], (
            TestLexer,
            TestParserEnglish
        )

        for test_case in test_cases:
            test_suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
            test_suites.append(test_suite)

        # run tests
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(test_suites))
        sys.exit(not result.wasSuccessful())
