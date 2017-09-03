#!/usr/bin/env python

__all__ = [
    '__program__',
    '__version__',
    '__license__',
    '__logo__'
]

__program__ = 'hmdc'
__version__ = '1.0.0-alpha'
__license__ = 'MIT'

__logo__ = r'''
  _                   _
 | |__  _ __ ___   __| | ___
 | '_ \| '_ ` _ \ / _` |/ __|
 | | | | | | | | | (_| | (__
 |_| |_|_| |_| |_|\__,_|\___|

 HMD-Compiler (%s)
 https://git.io/v5EWW

''' % (__version__)

# -t, --test
def run_all_tests():
    ''' run test suite.
    '''
    test_suites, test_cases = [], (
        # TestLexer,
        # TestParserEnglish
    )

    for test_case in test_cases:
        test_suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        test_suites.append(test_suite)

    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(test_suites))
    sys.exit(not result.wasSuccessful())
