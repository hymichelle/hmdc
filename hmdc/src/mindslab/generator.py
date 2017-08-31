#!/usr/bin/env python

from src.abstract.generator.generator import AbstractGenerator
from src.abstract.automata.automata import *
from src.abstract.parser.parser import *
from src.abstract.lexer.token import *
from src.abstract.lexer.lexer import *
from src.mindslab.grammar import *
from src.mindslab.syntax import *
from src.debug import *

import sys
import re

class HMDGenerator(AbstractGenerator):

    def __init__(self, optimization=False):

        # static
        self.syntax = HMDSyntaxDefault
        self.grammar = HMDGrammar()

        # initialize
        self.lexer = AbstractLexer(self.syntax)
        self.parser = AbstractParser(self.grammar)

        # flags
        self.optimization = optimization

        # temporary states
        self.tokens = None
        self.hmd = None
        self.code = None
        self.matrix = None

    #
    # public
    #

    def generate(self, lines=[]):
        '''
        '''
        if not lines: return []
        self.__initialize_hmd(lines)

        # delete all comments
        self.__remove_comments()

        # extract categories
        categories = self.__extract_categories()
        definitions = self.__extract_definitions()

        # lex
        self.tokens = self.lexer.lex(definitions)

        # parse
        self.code = self.parser.parse(self.tokens)

    #
    # private
    #

    def __initialize_hmd(self, lines=[]):
        self.hmd = sorted([ line.strip() for line in lines ]) # clean up lines

    def __remove_comments(self):
        comment = self.syntax.get('COMMENT') or '#' # token
        self.hmd = filter(lambda x:not re.findall(r'^%s.+$' % comment, x), self.hmd)

    def __extract_categories(self):
        return [ hmd.split('\t')[:-1] for hmd in self.hmd  if hmd[0] != '$' ]

    def __extract_definitions(self):
        return [ hmd.split('\t')[-1] for hmd in self.hmd ]

    def __build_matrix(self, hmd):
        return

    def __sort_definition(self, hmd):
        return
