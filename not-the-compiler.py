#!/usr/bin/env python3

from K4Lexer import K4Lexer
from K4Parser import K4Parser

test = """module testing
record x:
    int8 position
    byte[2] id
#        0x0F
#    0b_01_01
#0o765
"""
k4_lex = K4Lexer().clone()
k4_lex.input(test)
for i in k4_lex:
    print(i)

print()

k4_parser = K4Parser()
ast = k4_parser.parse(test)
print(ast)
