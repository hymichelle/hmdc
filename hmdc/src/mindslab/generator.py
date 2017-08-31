#!/usr/bin/env python

from src.abstract.generator.generator import AbstractGenerator
from src.abstract.automata.automata import *
from src.abstract.parser.parser import *
from src.abstract.lexer.token import *
from src.abstract.lexer.lexer import *
from src.mindslab.grammar import *
from src.mindslab.syntax import *
from src.debug import *

class HMDGenerator(AbstractGenerator):

    def __init__(self):
        self.lexer = AbstractLexer(HMDSyntaxDefault)
        self.parser = AbstractParser(HMDGrammar())
