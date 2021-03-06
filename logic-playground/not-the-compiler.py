#!/usr/bin/env python3

from K4Lexer import K4Lexer
from K4Parser import K4Parser

test = r"""module testing
facts:
    parent(me, isaac)
    parent(me, rosalind)
    parent(anne, isaac)
    parent(anne, rosalind)
    female(anne)
    male(me)
    male(isaac)
    female(rosalind)
    
constraint rules:
   daughtersFather(x) := parent(d, x) && female(x) && male(d)
"""
k4_lex = K4Lexer().clone()
k4_lex.input(test)
#for i in k4_lex:
#    print(i)
#print()

k4_parser = K4Parser()
ast = k4_parser.parse(test, debug=1)
print(ast)
