#!/usr/bin/env python

from collections import deque

import weakref

class AbstractAutomata(object):
    ''' an abstract automata that stores state, transition(s), start and end state.
    + state {str} -- a state.
    + transition {list} -- transition from a state to another state.
    + basetype {str} -- first-generation primitive type.
    + start {bool} -- initial/starting state (q_0).
    + final {bool} -- final/accepting state (q_f).
    '''

    def __init__(self, state='', transition=[], basetype='', start=False, final=False):
        self.state = state
        self.transition = transition
        self.basetype = basetype
        self.start = start
        self.final = final

class AbstractAutomataMachine(object):
    ''' an abstract machine that stores automata.
    '''

    def __init__(self):
        self.cache = deque()

    def __len__(self):
        return len(self.cache)

    #
    # public
    #

    def get_all_states(self):
        ''' get the state of all automata.
        '''
        return map(lambda x:x.state, self.cache)

    def get_transitions(self, state):
        ''' get defined transition(s) for a state in grammar.
        + state {AbstractAutomata} -- a particulra automata.
        '''
        automata = filter(lambda x:x.state == state, self.cache)
        return (automata[0].transition if len(automata) else None)

    def get_all_transitions(self):
        ''' get all possible transitions of automata.
        '''
        return map(lambda x:x.transition, self.cache)

    def set_states(self, machine=[]):
        ''' override automata with user-input.
        + states {AbstractAutomataMachine} -- an abstract finite automata.
        '''
        if all(map(lambda x:isinstance(x, AbstractAutomata), machine)):
            self.cache = machine
        return self.cache == machine

    def add_state(self, automata):
        ''' add automata state.
        + automata {AbstractAutomata} -- an automata.
        '''
        if not isinstance(automata, AbstractAutomata): return
        else:
            self.cache.append(automata)
            return weakref.ref(automata)
