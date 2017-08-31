#!/usr/bin/env python

from src.abstract.automata.automata import AbstractAutomataMachine
from src.debug import *

from collections import deque
import sys
import re

class AbstractParser(object):
    ''' an abstract parser to convert tokens into build instruction code.
    + grammar {AbstractAutomataMachine} -- grammar to check and parse tokens.
    '''

    def __init__(self, grammar):

        # grammar
        self.grammar = grammar.get_automata()
        self.variables = {}

        # stacks
        self.q_t = deque([None, None], maxlen=2) # circular queue
        self.q_b = []

        # build instruction
        self.code = deque()

    #
    # public
    #

    def parse(self, tokens):
        return self.__parse_definition(tokens)

    #
    # private
    #

    def __parse_definition(self, tokens=[]):
        ''' prototype to parse single definition tokens.
        + tokens {list} -- list of tokens from lexer.
        '''
        if len(tokens) < 2:
            debug('w', "TOKEN ERROR: not enough tokens to parse.\n")
            sys.exit(1)

        # definition construction
        token_peek, token_end = [tokens[0], tokens[-1]]
        if token_peek.type == 'RULE_BEGIN' and token_end.type == 'RULE_END': pass

        # variable
        elif token_peek.type == 'VARIABLE_IDENTIFIER':

            var = "".join([ token.value for token in tokens ])

            # variable identifier
            try: v_i = re.findall("^\$[A-Za-z]{1}\w*", var)[0][1:].strip()
            except IndexError:
                debug('w', "SYNTAX ERROR: variable must be alphabet only.\n")
                sys.exit(1)

            # retrieval?
            if not '=' in var and v_i in self.variables.keys():
                # replace
                pass

            # variable definition
            try: v_t = var[var.index('=')+1:var.index('#')] # comment
            except ValueError: v_t = var[var.index('=')+1:]

            # store variable
            self.variables[v_i] = v_t.strip()
            return True
        else:
            self.q_t.append(token_peek) # debug
            self.q_t.append(token_end) # debug
            self.__throw_syntax_error()

        # populate definition
        self.q_t.append(token_peek)
        for token in tokens[1::]:
            self.q_t.append(token)

            # check syntax
            if not self.__is_valid_syntax():
                self.__throw_syntax_error()

            # consolidate tokens
            self.__consolidate_tokens(token)

        # add instruction
        self.code.append(self.q_b[:])
        self.q_b[:] = [] # clear
        return True

    def __is_valid_syntax(self):
        ''' prototype to check for transition correctness.
        '''
        q_s, q_e = [self.q_t[0], self.q_t[1]] # queue start and end
        if not (q_s or q_e):
            return False

        # check valid transition
        try: return q_e.type in self.grammar.get_transitions(q_s.type)
        except: return False

    def __consolidate_tokens(self, token):
        ''' prototype to build instruction blocks.
        '''
        if not token or token.type in ['RULE_BEGIN', 'RULE_END']: return
        else: self.q_b.append(token.value)

    #
    # error
    #

    def __throw_syntax_error(self, tokens=[]):
        ''' print syntax error message.
        '''
        debug('w', "SYNTAX ERROR: 'NEXT TOKEN' is not valid:\n")
        self.__print_stack()
        sys.exit(1)

    #
    # debug
    #

    def __print_stack(self):
        sys.stdout.write("=> CURRENT TOKEN: %s\n" % (self.q_t[0] or {}) + \
                         "=> NEXT TOKEN:    %s\n" % (self.q_t[1] or {}))
