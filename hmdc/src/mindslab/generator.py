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

        # delete all comments
        self.__remove_comments()
        if not self.hmd: return

        # extract lines
        schemas = []
        for line in self.hmd:
            schema = HMDSchema()
            schema.pack(line)
            schemas.append(schema)

        # consolidate
        categories = filter(len, map(lambda x:x.category, schemas))
        definitions = map(lambda x:x.definition, schemas)

        # lex
        self.tokens = self.lexer.lex(definitions)

        # parse
        self.code = self.parser.parse(self.tokens)

        # permute
        hmd = self.__permute_data(self.__merge_data(categories, self.code))

        # build matrix
        return self.__build_matrix(hmd)

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
        token = self.syntax.get('COMMENT', '#') # default
        if self.hmd:
            self.hmd = filter(lambda x:not re.findall(r'^%s.+$' % token, x), self.hmd)

    def __merge_data(self, categories=[], definitions=[]):
        ''' merge categories and definitions to matrix.
        '''
        if categories and len(categories) == len(definitions):
            return zip(categories, self.code)
        return [None, None]

    def __permute_data(self, merged=[]):
        ''' permute two lists.
        '''
        return merged

    def __build_matrix(self, hmd=[[],'']):
        ''' build matrix from hmd data.
        '''
        if not hmd: return ''
        matrix = []

        # standardize category count
        categories_cnt = min(max(map(lambda x:len(x[0]), hmd)), self.max_categories) # find the smallest
        for i in range(len(hmd)):

            # schema
            hmd_peek = list(hmd[i])
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
