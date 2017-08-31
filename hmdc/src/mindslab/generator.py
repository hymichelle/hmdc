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
    ''' default hierarchial multiple dictionary generator.
    '''

    def __init__(self, max_categories=10, optimization=False):

        # static
        self.syntax = HMDSyntaxDefault
        self.grammar = HMDGrammar()

        # initialized classes
        self.lexer = AbstractLexer(self.syntax)
        self.parser = AbstractParser(self.grammar)

        # flags
        self.optimization = optimization or False

        # build options
        self.max_categories = max_categories

        # temporary states
        self.tokens = None
        self.hmd = None
        self.code = None
        self.matrix = None

    #
    # public
    #

    def generate(self, lines=[]):
        ''' compile hmd dictionary to matrix form.
        '''
        if not lines: return []
        self.__initialize_hmd(lines)

        # delete all comments
        self.__remove_comments()

        # extract categories
        categories, definitions = [], []
        for data in self.__extract_data():
            categories.append(data[0])
            definitions.append(data[-1])

        # lex
        self.tokens = self.lexer.lex(definitions)

        # parse
        self.code = self.parser.parse(self.tokens)

        # build matrix
        merged = self.__merge_data(filter(len, categories), self.code)
        return self.__build_matrix(merged)

    #
    # private
    #

    def __initialize_hmd(self, lines=[]):
        ''' initialize input lines to workable format.
        '''
        try: self.hmd = sorted([ line.strip() for line in lines ]) # clean up
        except:
            debug('w', "unable to sanitize input => check input for string type.\n")
            sys.exit(1)

    def __remove_comments(self):
        ''' remove all commented lines.
        '''
        token = self.syntax.get('TOKEN') or '#' # default
        if self.hmd:
            self.hmd = filter(lambda x:not re.findall(r'^%s.+$' % token, x), self.hmd)

    def __extract_data(self):
        ''' split definitions from categories in session hmd data.
        '''
        if not self.hmd: return ['','']
        token = self.syntax.get('VARIABLE_IDENTIFIER') or '$' # default
        table = []
        for hmd in self.hmd:

            # store non-variables
            if hmd[0] not in token:
                hmd = hmd.split('\t')
                table.append([
                    hmd[:-1], # categories
                    hmd[-1] # definition
                ])

            # store variables
            else: table.append(['',hmd])
        return table

    def __merge_data(self, categories=[], definitions=[]):
        ''' merge categories and definitions to matrix.
        '''
        if categories and len(categories) == len(definitions):
            return zip(categories, self.code)
        return [None,None]

    def __build_matrix(self, hmd=[[],'']):
        ''' build matrix from hmd data.
        '''
        if not hmd: return ''
        matrix = []

        # standardize category count
        categories_cnt = min(max(map(lambda x:len(x[0]), hmd)), self.max_categories) # find the smallest
        for i in range(len(hmd)):

            hmd_peek = list(hmd[i])
            category = hmd_peek[0]
            definition = hmd_peek[-1]

            # normalize category count
            deviation = int(len(category) - categories_cnt)
            category.extend([''] * (0 - deviation)) # distance from origin

            # compile matrix
            category = '\t'.join(category)
            definition = '$'.join(definition[1:-1].split(')('))
            matrix.append('\t'.join([category, definition]))

        return '\n'.join(matrix)
