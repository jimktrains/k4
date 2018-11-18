#/usr/bin/env python3

import ply.yacc as yacc
import K4Lexer
from K4AST import Record, Definition, Module, Enum, EnumValue, Number

tokens = K4Lexer.tokens

def K4Parser():
    start = 'module'

    def p_module(p):
        ''' module : MODULE ID NEWLINE complex_declaration_list
        '''
        p[0] = Module(p[2], p[4])

    def p_complex_declaration_list(p):
        ''' complex_declaration_list : complex_declaration
                                   | complex_declaration_list complex_declaration '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_complex_declaration(p):
        ''' complex_declaration : record
                              | enum
                              | simple_declaration
                              | func
        '''
        p[0] = p[1]

    def p_func(p):
        ''' func : FUNC name COLON statement_list
        '''

    def p_simple_declaration(p):
        ''' simple_declaration : definition
        '''
        p[0] = p[1]

    def p_assigment(p):
        ''' assigment : ID ASSIGN assigment_value '''
        p[0] = Assign(p[1], p[3])

    def p_assigment_value(p):
        ''' assigment_value : empty
                            | ID
                            | number
        '''
        if len(p) >= 2:
            p[0] = p[1]

    def p_record(p):
        ''' record : RECORD ID COLON INDENT definition_list DEDENT'''
        p[0] = Record(p[2], p[5])

    def p_enum(p):
        ''' enum : ENUM ID OPEN_ANGLE_BRACKET storage_type CLOSE_ANGLE_BRACKET COLON INDENT enum_value_list DEDENT '''
        p[0] = Enum(p[2], p[4], p[8])

    def p_enum_value_list(p):
        ''' enum_value_list : enum_value
                          | enum_value_list NEWLINE enum_value
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_enum_value(p):
        ''' enum_value : ID DEFINE number '''
        p[0] = EnumValue(p[1], p[3])

    def p_definition_list(p):
        ''' definition_list : definition
                            | definition_list NEWLINE definition
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        
    def p_definition(p):
        ''' definition : type ID definition_value '''
        v = 0
        if len(p) == 5:
            v = p[4]
        p[0] = Definition(p[1], p[2])

    def p_definition_value(p):
        ''' definition_value : empty
                             | DEFINE assigment_value '''
        if len(p) == 3:
            p[0] = p[2]

    def p_empty(p):
        ''' empty : '''
        pass

    def p_storage_type(p):
        ''' storage_type : BYTE
                         | NIBBLE
        '''
        p[0] = p[1]

    def p_type(p):
        ''' type : INT8
                 | BYTE
                 | BYTE OPEN_SQUARE_BRACKET number CLOSE_SQUARE_BRACKET
                 | ID
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('buffer', p[3])

    def p_number(p):
        ''' number : NUMBER '''
        p[0] = Number(p[1])

    def p_error(p):
        if p and p.type == "NEWLINE":
            parser.errok()
            return
        print("Syntax error in input!")
        print(p)
        print("line = ", p.lexer.lineno)

    parser = yacc.yacc()

    return parser
