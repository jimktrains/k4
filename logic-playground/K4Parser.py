#/usr/bin/env python3

import ply.yacc as yacc
import K4Lexer
from K4AST import *

tokens = K4Lexer.tokens

def K4Parser():
    start = 'module'

    def p_module(p):
        ''' module : MODULE ID NEWLINE facts constraint_rules
        '''
        p[0] = Module(p[2], p[4], p[5])

    def p_facts(p):
        ''' facts : FACTS COLON INDENT fact_list DEDENT
        '''
        p[0] = Facts(p[4])

    def p_fact_list(p):
        ''' fact_list : fact
                      | fact_list NEWLINE fact'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    def p_fact(p):
        ''' fact : ID OPEN_PARENTHESIS fact_term_list CLOSE_PARENTHESIS
        '''
        p[0] = Fact(p[1], p[3])
    def p_fact_term_list(p):
        ''' fact_term_list : fact_term
                           | fact_term_list COMMA fact_term
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    def p_fact_term(p):
        ''' fact_term : atom
                      | variable
                      | number
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + [p[3]]

    def p_variable(p):
        ''' variable : ID '''
        p[0] = Variable(p[1])

    def p_constraint_rules(p):
        ''' constraint_rules : CONSTRAINT RULES COLON INDENT constraint_rule_list DEDENT
        '''
        p[0] = ConstraintRules(p[5])
    def p_constraint_rule_list(p):
        ''' constraint_rule_list : constraint_rule
                                 | constraint_rule_list NEWLINE constraint_rule'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_constraint_rule(p):
        ''' constraint_rule : ID OPEN_PARENTHESIS id_list CLOSE_PARENTHESIS DEFINE constraint_expression
        '''
        p[0] = ConstraintRule(p[1], p[3], p[6])

    def p_id_list(p):
        ''' id_list : ID
                    | id_list COMMA ID
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_constraint_call(p):
        ''' constraint_call : ID OPEN_PARENTHESIS id_list CLOSE_PARENTHESIS
        '''
        p[0] = ConstraintCall(p[1], p[3])

    def p_constraint_expression(p):
        ''' constraint_expression : atom
                                  | term
                                  | constraint_call
                                  | constraint_expression logical_op constraint_expression
                                  | OPEN_PARENTHESIS constraint_expression CLOSE_PARENTHESIS
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = ConstraintExpression(p[1], p[2], p[3])

    def p_atom(p):
        ''' atom : ATOM '''
        p[0] = Atom(p[1])

    def p_term(p):
        ''' term : ID '''
        p[0] = Term(p[1])

    def p_logical_op(p):
        ''' logical_op : LOGICAL_AND
                       | LOGICAL_OR
                       | LOGICAL_XOR
                       | LOGICAL_IMPLICATION
                       | LOGICAL_BICONDITIONAL
                       | LOGICAL_EQUALITY
        '''
        p[0] = p[1]

    #def p_func(p):
    #    ''' func : FUNC name COLON statement_list
    #    '''

    #def p_simple_declaration(p):
    #    ''' simple_declaration : definition
    #    '''
    #    p[0] = p[1]

    #def p_assigment(p):
    #    ''' assigment : ID ASSIGN assigment_value '''
    #    p[0] = Assign(p[1], p[3])

    #def p_assigment_value(p):
    #    ''' assigment_value : empty
    #                        | ID
    #                        | number
    #    '''
    #    if len(p) >= 2:
    #        p[0] = p[1]

    #def p_record(p):
    #    ''' record : RECORD ID COLON INDENT definition_list DEDENT'''
    #    p[0] = Record(p[2], p[5])

    #def p_enum(p):
    #    ''' enum : ENUM ID OPEN_ANGLE_BRACKET storage_type CLOSE_ANGLE_BRACKET COLON INDENT enum_value_list DEDENT '''
    #    p[0] = Enum(p[2], p[4], p[8])

    #def p_enum_value_list(p):
    #    ''' enum_value_list : enum_value
    #                      | enum_value_list NEWLINE enum_value
    #    '''
    #    if len(p) == 2:
    #        p[0] = [p[1]]
    #    else:
    #        p[0] = p[1] + [p[3]]

    #def p_enum_value(p):
    #    ''' enum_value : ID DEFINE number '''
    #    p[0] = EnumValue(p[1], p[3])

    #def p_definition_list(p):
    #    ''' definition_list : definition
    #                        | definition_list NEWLINE definition
    #    '''
    #    if len(p) == 2:
    #        p[0] = [p[1]]
    #    else:
    #        p[0] = p[1] + [p[3]]
    #    
    #def p_definition(p):
    #    ''' definition : type ID definition_value '''
    #    v = 0
    #    if len(p) == 5:
    #        v = p[4]
    #    p[0] = Definition(p[1], p[2])

    #def p_definition_value(p):
    #    ''' definition_value : empty
    #                         | DEFINE assigment_value '''
    #    if len(p) == 3:
    #        p[0] = p[2]

    #def p_empty(p):
    #    ''' empty : '''
    #    pass

    #def p_storage_type(p):
    #    ''' storage_type : BYTE
    #                     | NIBBLE
    #    '''
    #    p[0] = p[1]

    #def p_type(p):
    #    ''' type : INT8
    #             | BYTE
    #             | BYTE OPEN_SQUARE_BRACKET number CLOSE_SQUARE_BRACKET
    #             | ID
    #    '''
    #    if len(p) == 2:
    #        p[0] = p[1]
    #    else:
    #        p[0] = ('buffer', p[3])

    def p_number(p):
        ''' number : NUMBER '''
        p[0] = Number(p[1])

    def p_error(p):
        if p and p.type == "NEWLINE":
            parser.errok()
            return
        if p and p.type == "DEDENT":
            parser.errok()
            return
        print("Syntax error in input!")
        print(p)
        print("line = ", p.lexer.lineno)

    parser = yacc.yacc()

    return parser
