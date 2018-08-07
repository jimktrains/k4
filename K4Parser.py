#/usr/bin/env python3

import ply.yacc as yacc
import K4Lexer
from K4AST import Record, Definition, Module

tokens = K4Lexer.tokens

def K4Parser():
    start = 'module'

    def p_module(p):
        ''' module : MODULE ID record
        '''
        module = Module(p[2], [p[3]])
        p[0] = module

    def p_record(p):
        ''' record : RECORD ID COLON INDENT definition_list DEDENT'''
        record = Record(p[2], p[5])
        p[0] = record

    def p_definition_list(p):
        ''' definition_list : definition
                            | definition_list NEWLINE definition
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        
    def p_definition(p):
        ''' definition : type ID '''
        definition = Definition(p[1], p[2])
        p[0] = definition

    def p_type(p):
        ''' type : INT8
                 | BYTE
                 | BYTE OPEN_SQUARE_BRACKET NUMBER CLOSE_SQUARE_BRACKET '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('buffer', p[3])

    def p_error(p):
        if p and p.type == "NEWLINE":
            parser.errok()
            return
        print("Syntax error in input!")
        print(p)
        print("line = ", p.lexer.lineno)

    parser = yacc.yacc()

    return parser
