#!/usr/bin/env python

from src.abstract.automata.automata import AbstractAutomata, AbstractAutomataMachine
from src.abstract.generator.generator import AbstractGenerator
from src.abstract.parser.parser import AbstractParser
from src.abstract.lexer.token import AbstractToken
from src.abstract.lexer.lexer import AbstractLexer
from src.mindslab.grammar import HMDGrammar
from src.mindslab.syntax import *
from src.debug import *

import itertools
import sys
import re

class HMDSchema(object):
    ''' an abstract schema for a valid hmd line.
    '''

    def __init__(self, category=[], definition=''):

        # static
        self.syntax = HMDSyntaxDefault

        # state
        self.category = category
        self.definition = definition

    def pack(self, line=''):
        ''' extract a line into hmd schema.
        '''
        if not line:
            self.category = []
            self.definition = ''
            return

        identifier = self.syntax.get('VARIABLE_IDENTIFIER', '$') # default
        if identifier not in line:
            tokens = line.split('\t')
            self.category = tokens[:-1]
            self.definition = tokens[-1]
        else:
            self.category = ['']
            self.definition = line

    def unpack(self):
        ''' unpack a line into category and definition.
        '''
        return (self.category, self.definition)

class HMDGenerator(AbstractGenerator):
    ''' default hierarchial multiple dictionary generator.
    '''

    def __init__(self, max_categories=10, optimization=False):

        # static
        self.syntax = HMDSyntaxDefault
        self.grammar = HMDGrammar()

        # initialization
        self.lexer = AbstractLexer(self.syntax)
        self.parser = AbstractParser(self.grammar)

        # build options
        self.max_categories = max_categories
        self.optimization = optimization

        # temporary states
        self.hmd = None
        self.matrix = None

    #
    # public
    #

    def generate(self, lines=[]):
        ''' compile hmd dictionary to matrix form.
        '''
        if not lines: return
        self.__initialize_hmd(lines)

        # delete comments
        self.__remove_comments()
        if not self.hmd: return

        # divide lines into hmd-schema
        schemas = []
        for hmd in self.hmd:
            schema = HMDSchema()
            schema.pack(hmd)
            schemas.append(schema)

        # categories must be length-filtered due to variables
        categories = filter(len, [ schema.category for schema in schemas ])
        definitions = [ schema.definition for schema in schemas ]

        # parse and generate matrix
        tokens = self.lexer.lex(definitions)
        definitions = self.parser.parse(tokens)
        return self.__build_matrix(categories, definitions)

    #
    # private
    #

    def __initialize_hmd(self, lines=[]):
        ''' initialize self.hmd with raw lines.
        + lines {list} -- lines to convert from hmd to matrix.
        '''
        try: self.hmd = [ line.strip() for line in lines ]
        except:
            debug('w', 'GENERATOR: unable to sanitize input for string type.\n')
            sys.exit(1)

    def __remove_comments(self):
        ''' remove all commented lines.
        '''
        if not self.hmd: return
        comments = r'^%s.+$' % self.syntax.get('COMMENT', '#')
        self.hmd = filter(lambda x:not re.findall(comments, x), self.hmd)

    def __flatten(self, L=[]):
        ''' recursively flatten nested lists/tuples.
        + L {list|tuple} -- nested list/tuple.
        '''
        if not L: return L
        if isinstance(L[0], tuple) or isinstance(L[0], list):
            return self.__flatten(L[0]) + self.__flatten(L[1:])
        return L[:1] + self.__flatten(L[1:])

    def __permute(self, category=[], definition=''):
        ''' get cartesian product of definitions and pair with category.
        + category {list} -- a list of category.
        + definition {list} -- definition.
        '''
        try: blocks = definition[1:-1].split(')(')
        except IndexError: blocks = []
        if not blocks: return blocks

        # tokenize into sets
        s_p, s_q = [], []
        for block in blocks:
            if '|' in block: s_p.append(block.split('|'))
            else: s_q.append(block)

        # find cartesian product
        if s_p:
            nested =  [ product for product in reduce(lambda x,y:itertools.product(x,y), s_p) ]
            product = map(list, [ self.__flatten(nest) for nest in nested ])

            # pair with categories
            try: permutation = [ [category, '(%s)' % ')('.join(pairable + s_q)] for pairable in product ]
            except: permutation = []
        else: permutation = [[category, definition]]
        return permutation

    def __build_matrix(self, categories=[], definitions=[]):
        ''' build matrix from hmd data.
        + categories {list} -- a list of categories.
        + definitions {list} -- a list of definitions.
        '''
        try: assert bool(categories) and len(categories) == len(definitions)
        except AssertionError:
            debug('b', 'GENERATOR: uneven data merge.\n')
            sys.exit(1)

        # standardize category count
        matrix = []
        categories_cnt = min(max(map(len, categories)), self.max_categories) # find the smallest
        for i in xrange(len(categories)):

            # schema
            category, definition = categories[i], definitions[i]

            # normalize category count
            deviation = int(len(category) - categories_cnt)
            distance = 0 - deviation # distance from origin
            if deviation >= 0: category.extend([''] * distance)
            else:
                partition = abs(distance - 1)
                category = category[partition:].append("_".join(category[:partition]))

            # compile matrix
            for permutation in self.__permute(category, definition):
                if not permutation: pass
                category, definition = permutation
                matrix.append('\t'.join([
                    '\t'.join(category), # category
                    '$'.join(definition[1:-1].split(')(')) # definition
                ]))

        return '\n'.join(matrix)
