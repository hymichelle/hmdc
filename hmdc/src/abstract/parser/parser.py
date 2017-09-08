#!/usr/bin/env python

from src.abstract.automata.automata import AbstractAutomataMachine
from src.abstract.lexer.token import AbstractToken
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
        self.code = []

    #
    # public
    #

    def parse(self, tokens=[]):
        ''' prototype to parse lexed single line string or a list of strings.
        + tokens {str|list[list]} -- list or nested lists of tokens.
        '''
        if not tokens: return []
        if not all(isinstance(token, list) for token in tokens): self.eval(tokens) # tokens
        else: [ self.eval(token) for token in tokens ] # nested tokens
        return self.code or []

    def eval(self, tokens=[]):
        ''' prototype to parse single line of tokens.
        + tokens {list} -- list of tokens from lexer.
        '''
        if len(tokens) < 2 or not all(map(lambda token:isinstance(token, AbstractToken), tokens)):
            debug('w', 'PARSER: not enough tokens or not abstract tokens.\n')
            self.code = None
            return

        try: line = ''.join([ token.value for token in tokens ])
        except:
            debug('b', 'PARSER: invalid value type in tokens.\n')
            self.code = None
            return

        if '$' in line:

            # find all unique identifiers
            identifiers = set(re.findall('\$[A-Za-z]{1}\w*', line))

            # store/interpolate identifiers
            for v_i in identifiers:
                if '=' in line:
                    try: v_d = tokens[line.index('=')+1:line.index('#')] # upto comment
                    except ValueError: v_d = tokens[line.index('=')+1:] # upto EOL
                    self.variables[v_i] = v_d
                else:
                    if v_i in self.variables.keys():
                        index = [ x.start() for x in re.finditer('\%s' % v_i, line) ] # escape '\$'
                        for i in index: tokens = tokens[:i] + self.variables[v_i] + tokens[i+len(v_i):]
                        self.__parse_tokens(tokens)
                    else:
                        debug('w', "variable '%s' is not defined.\n" % v_i)
                        self.code = None
                        return

        # parse definition
        elif tokens[0].type == 'RULE_BEGIN' and tokens[-1].type == 'RULE_END':
            try: self.__parse_tokens(tokens)
            except:
                self.q_t.append(tokens[0]) # debug
                self.q_t.append(tokens[-1]) # debug
                self.__throw_syntax_error()

        else:
            self.q_t.append(tokens[0]) # debug
            self.q_t.append(tokens[-1]) # debug
            self.__throw_syntax_error()

    #
    # private
    #

    def __parse_tokens(self, tokens=[]):
        ''' prototype to parse tokens and add to code instruction.
        + tokens {list} -- list of tokens from lexer.
        '''
        if len(tokens) < 2:
            debug('w', "PARSER ERROR: there must be 2+ tokens to parse into matrix.\n")
            return

        self.q_t.append(tokens[0])
        self.__consolidate_tokens(tokens[0])

        for token in tokens[1::]:
            self.q_t.append(token)

            # check syntax
            if not self.__is_valid_syntax():
                self.__throw_syntax_error()
                return

            # consolidate tokens
            self.__consolidate_tokens(token)

        # add instruction
        self.code.append("".join(self.q_b[:]))
        self.q_b[:] = [] # clear

    def __is_valid_syntax(self):
        ''' prototype to check for transition correctness.
        '''
        q_s, q_e = [self.q_t[0], self.q_t[1]] # queue start and end
        if not (q_s or q_e):
            return

        # check valid transition
        try: return q_e.type in self.grammar.get_transition(q_s.type)
        except: return

    def __consolidate_tokens(self, token):
        ''' prototype to build instruction blocks.
        '''
        self.q_b.append(token.value)

    #
    # error
    #

    def __throw_syntax_error(self, tokens=[]):
        ''' print syntax error message.
        '''
        debug('w', "SYNTAX ERROR: 'next' token is not a valid definition or transition:\n")
        self.__print_stack()

    #
    # debug
    #

    def __print_stack(self):
        sys.stdout.write("=> curret: %s\n" % (self.q_t[0] or {}) + \
                         "=> next:   %s\n" % (self.q_t[1] or {}))
