#!/usr/bin/env python

class AbstractGenerator(object):
    '''an abstract generator that builds compiled code.
    '''

    def __init__(self):
        self.machine = None

    def generate(self, machine):
        '''
        : machine {AbstractAutomataMachine} -- automata machine.
        '''
        self.machine = machine
        super(type(self.__build__))
        return self.__build__()

    def __build__(self):
        # override
        pass
