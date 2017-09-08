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

    def test_parser_empty_string(self):
        attempt = self.parser.parse('')
        answer = []
        self.assertEqual(attempt, answer)

    def test_parser_empty_list(self):
        attempt = self.parser.parse([])
        self.assertFalse(attempt)

    def test_parser_empty_list_string(self):
        attempt = self.parser.parse([''])
        self.assertFalse(attempt)

    def test_parser_empty_list_strings(self):
        attempt = self.parser.parse(['',''])
        self.assertFalse(attempt)

    #
    # syntax: valid
    #

    #
    # syntax: invalid
    #

    def test_parser_invalid_syntax_empty(self):
        hmd = '()'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_leading_double(self):
        hmd = '(()'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_trailing_double(self):
        hmd = '())'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_nested(self):
        hmd = '(())'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_sequel(self):
        hmd = '+'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_sequels(self):
        hmd = '++'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_sequel_missing_count(self):
        hmd = '(+)'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_sequel_missing_count_nested(self):
        hmd = '(+())'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_sequel_leading_missing_count(self):
        hmd = '+()'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_sequel_trailing_missing_count(self):
        hmd = '()+'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_prequel(self):
        hmd = '-'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_prequels(self):
        hmd = '--'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_prequel_missing_count(self):
        hmd = '(-)'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_prequel_missing_count_nested(self):
        hmd = '(-())'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_prequel_leading_missing_count(self):
        hmd = '-()'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_prequel_trailing_missing_count(self):
        hmd = '()-'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_following(self):
        hmd = '@'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_followings(self):
        hmd = '@@'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_following_missing_count(self):
        hmd = '(@)'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_following_missing_count_nested(self):
        hmd = '(@())'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_following_leading_missing_count(self):
        hmd = '@()'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)

    def test_parser_invalid_syntax_following_trailing_missing_count(self):
        hmd = '()@'
        tokens = self.lexer.lex(hmd)
        attempt = self.parser._AbstractParser__parse_definition(tokens)
        self.assertFalse(attempt)
