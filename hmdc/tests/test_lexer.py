#!/usr/bin/env python

from src.abstract.lexer.token import AbstractToken
from src.abstract.lexer.lexer import *

import unittest

class TestLexer(unittest.TestCase):
    '''
    : unit tests for lexer class.
    '''

    lexer = AbstractLexer()

    def test_lexer_string_blank(self):
        attempt = self.lexer.lex('')
        answer = []
        self.assertEqual(attempt, answer)
