#!/usr/bin/env python

from abstract.lexer.token import *
from abstract.lexer.lexer import *

import unittest

class TestLexer(unittest.TestCase):
    '''
    : unit tests for token class.
    '''

    lexer = AbstractLexer()

    def test_lexer_string_mixed(self):

        # attempt
        attempt = self.lexer.lex('a1@ ')

        # answer
        answer = r"[token={'y': -1, 'x': -1, 'type': 'string', 'value': 'a'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'number', 'value': '1'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'symbol', 'value': '@'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'space', 'value': ' '}]"

        self.assertEqual(str(attempt), answer)

    def test_lexer_string_escaped_strings(self):

        # attempt
        attempt = self.lexer.lex('\\dddd\n\t')

        # answer
        answer = r"[token={'y': -1, 'x': -1, 'type': None, 'value': '\\'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'd'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'd'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'd'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'd'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': None, 'value': '\n'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': None, 'value': '\t'}]"

        self.assertEqual(str(attempt), answer)

    def test_lexer_string_case_sensitive(self):

        # attempt
        attempt = self.lexer.lex('aAbBzZ0-9')

        # answer
        answer = r"[token={'y': -1, 'x': -1, 'type': 'string', 'value': 'a'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'A'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'b'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'B'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'z'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'string', 'value': 'Z'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'number', 'value': '0'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'symbol', 'value': '-'}, " +\
                  r"token={'y': -1, 'x': -1, 'type': 'number', 'value': '9'}]"

        self.assertEqual(str(attempt), answer)

    def test_lexer_string_blank(self):

        # attempt
        attempt = self.lexer.lex('')

        # answer
        answer = []

        self.assertEqual(attempt, answer)
