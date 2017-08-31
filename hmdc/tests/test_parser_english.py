#!/usr/bin/env python
#
# @author: Herbert Shin
# @maintainer: Herbert Shin
# @email: herbert@mindslab.ai
# @revision: 2017-06-20
# @license: MindsLab
#

from __future__ import absolute_import

from abstract.automata.automata import *
from abstract.parser.parser import *
from abstract.lexer.token import *
from abstract.lexer.lexer import *

from mindslab.grammar import HMDGrammarEnglish
from mindslab.syntax import HMDSyntaxEnglish

import unittest

class TestParserEnglish(unittest.TestCase):
    '''
    : unit tests for english parser class.
    '''

    grammar = HMDGrammarEnglish()
    syntax = HMDSyntaxEnglish()

    parser = AbstractParser(grammar)
    lexer = AbstractLexer(syntax.syntax)

    #
    # correct syntax
    #

    def test_parser_hmd_syntax_correct_mixed_characters(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(abAB22299)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_single_character(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_after_no_space_small(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(+3a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_after_no_space_large(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(+39849349a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_before_no_space_small(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(-3a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_before_no_space_large(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(-39849349a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_after_with_space_small(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(+3 a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_after_with_space_large(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(+39849349 a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_before_with_space_small(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(-3 a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_before_with_space_large(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(-39849349 a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_no_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(!a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_with_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(! a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_no_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(!A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_with_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(! A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_no_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(!10)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_with_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(! 10)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_no_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(!10aMx3)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_with_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(! 10aMx3)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_no_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(!aMx310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_with_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(! aMx310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_no_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(!Max310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_not_with_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(! Max310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_no_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_with_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_no_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_with_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_no_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%10)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_with_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% 10)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_no_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%10aMx3)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_with_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% 10aMx3)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_no_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%aMx310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_with_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% aMx310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_no_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%Max310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_with_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% Max310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_no_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_with_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@ a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_no_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_with_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@ A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_no_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@10)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_with_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@ 10)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_no_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@10aMx3)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_with_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@ 10aMx3)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_no_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@aMx310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_with_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@ aMx310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_no_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@Max310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_with_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(@ Max310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_hat_no_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(^0a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_hat_no_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(^0A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_hat_no_space_digit(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(^3a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_hat_with_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(^0 a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_hat_with_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(^0 A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_mixed_no_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@%a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_mixed_no_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@%A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_mixed_no_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@%10)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_mixed_no_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@%10aMx3)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_mixed_no_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@%aMx310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_always_mixed_no_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@%Max310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_mixed_no_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%@a)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_mixed_no_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%@A)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_mixed_no_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%@10)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_mixed_no_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%@10aMx3)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_mixed_no_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%@aMx310)'))
        self.assertTrue(attempt)

    def test_parser_hmd_syntax_correct_wild_mixed_no_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(%@Max310)'))
        self.assertTrue(attempt)

    #
    # incorrect syntax
    #

    def test_parser_hmd_syntax_incorrect_rule_empty(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'()'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_empty_space_small(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'( )'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_empty_space_large(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(      )'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_incomplete_opening(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(('))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_incomplete_closing(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'))'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_incomplete_half_opening(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(()'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_incomplete_half_closing(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'())'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_incomplete_full_closing(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(( ))'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_incomplete_nested_closing_filled(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(a))'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_incomplete_nested_opening_filled(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'((a)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_rule_complete_nested_rule(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'((a))'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_always_mixed_with_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@ % a)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_always_mixed_with_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@ % A)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_always_mixed_with_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@ % 10)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_always_mixed_with_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@ % 10aMx3)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_always_mixed_with_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@ % aMx310)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_always_mixed_with_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(@ % Max310)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_wild_mixed_with_space_lowercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% @ a)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_wild_mixed_with_space_uppercase(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% @ A)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_wild_mixed_with_space_digits(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% @ 10)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_wild_mixed_with_space_mixed_one(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% @ 10aMx3)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_wild_mixed_with_space_mixed_two(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% @ aMx310)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_wild_mixed_with_space_mixed_three(self):
        attempt = self.parser.check_syntax(self.lexer.lex(r'(% @ Max310)'))
        self.assertFalse(attempt)

    def test_parser_hmd_syntax_incorrect_hat_no_space_mixed(self):
        attempt = self.parser.check_syntax(self.lexer.lex('(^3A;)'))
        self.assertFalse(attempt)
