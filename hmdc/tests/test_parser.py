#!/usr/bin/env python

from src.abstract.automata.automata import AbstractAutomataMachine
from src.abstract.parser.parser import AbstractParser
from src.abstract.lexer.token import AbstractToken
from src.abstract.lexer.lexer import AbstractLexer
from src.mindslab.grammar import HMDGrammar
from src.mindslab.syntax import *

import unittest

class TestParser(unittest.TestCase):
    '''
    : unit tests for parser class.
    '''

    lexer = AbstractLexer(HMDSyntaxDefault)
    parser = AbstractParser(HMDGrammar())

    def test_parser_string_blank(self):
        tokens = self.lexer.lex('')
        attempt = self.parser.parse(tokens)
        answer = []
        self.assertEqual(attempt, answer)
