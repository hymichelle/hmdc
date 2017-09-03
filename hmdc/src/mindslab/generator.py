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
        self.tokens = self.lexer.lex(definitions)
        self.code = self.parser.parse(self.tokens)
        self.hmd = self.__permute(self.__merge(categories, self.code))
        return self.__build_matrix(self.hmd)

    #
    # private
    #

    def __initialize_hmd(self, lines=[]):
        ''' initialize self.hmd with raw lines.
        + lines {list} -- lines to convert from hmd to matrix.
        '''
        try: self.hmd = [ line.strip() for line in lines ]
        except:
            debug('w', "unable to sanitize input => check input for string type.\n")
            sys.exit(1)

    def __remove_comments(self):
        ''' remove all commented lines.
        '''
        if not self.hmd: return
        comments = r'^%s.+$' % self.syntax.get('COMMENT', '#')
        self.hmd = filter(lambda x:not re.findall(comments, x), self.hmd)

    def __merge(self, categories=[], definitions=[]):
        ''' merge categories and definitions to matrix.
        + categories {list} -- hmd categories from schema.
        + definitions {list} -- hmd definitions from schema.
        '''
        if categories and len(categories) == len(definitions):
            return zip(categories, self.code) # parsed definitions
        else:
            debug('w' '***bug***: incorrect merge: please check merging logic in generator.\n')
            sys.exit(1)

    def __permute(self, hmd_merged=[[],[]]):
        ''' permute two lists.
        + hmd_merged {list[list,list]} -- merged categories and definitions.
        '''
        return hmd_merged

    def __build_matrix(self, hmd_permuted=[[],'']):
        ''' build matrix from hmd_permuted data.
        + merged {list[list,list]} -- merged list categories and definitions.
        '''
        if not hmd_permuted: return ''
        matrix = []

        # standardize category count
        categories_cnt = min(max(map(lambda x:len(x[0]), hmd_permuted)), self.max_categories) # find the smallest
        for i in range(len(hmd_permuted)):

            # schema
            hmd_peek = list(hmd_permuted[i])
            category = hmd_peek[0]
            definition = hmd_peek[-1]

            # normalize category count
            deviation = int(len(category) - categories_cnt)
            distance = 0 - deviation # distance from origin
            if deviation >= 0:
                category.extend([''] * distance)
            else:
                partition = abs(distance - 1)
                category = category[partition:].append("_".join(category[:partition]))

            # compile matrix
            category = '\t'.join(category)
            definition = '$'.join(definition[1:-1].split(')('))
            matrix.append('\t'.join([category, definition]))

        return '\n'.join(matrix)
