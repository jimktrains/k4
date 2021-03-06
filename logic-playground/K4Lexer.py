#!/usr/bin/env python3

import ply.lex as lex
import re

tokens = [
        'NEWLINE',
        'OPEN_SQUARE_BRACKET',
        'CLOSE_SQUARE_BRACKET',
        'OPEN_PARENTHESIS',
        'CLOSE_PARENTHESIS',
        'PLUS',
        'MINUS',
        'ID',
        'ATOM',
        'COMMENT',
        'COMMA',
        'COLON',
        'SEMICOLON',
        'ASSIGN',
        'DEFINE',
        'OPEN_ANGLE_BRACKET',
        'CLOSE_ANGLE_BRACKET',
        'OPEN_BRACE',
        'CLOSE_BRACE',
        'INDENT',
        'DEDENT',
        'NUMBER',
        'WS',
        'AT',
        'DOLLAR',
        'LEFT_SHIFT',
        'RIGHT_SHIFT',
        'BITWISE_AND',
        'BITWISE_OR',
        'BITWISE_XOR',
        'LOGICAL_AND',
        'LOGICAL_OR',
        'LOGICAL_XOR',
        'LOGICAL_IMPLICATION',
        'LOGICAL_BICONDITIONAL',
        'LOGICAL_EQUALITY',
        ]

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_OPEN_PARENTHESIS  = r'\('
t_CLOSE_PARENTHESIS  = r'\)'
t_OPEN_SQUARE_BRACKET = r'\['
t_CLOSE_SQUARE_BRACKET = r'\]'
t_COLON = r':'
t_SEMICOLON = r';'
t_ASSIGN = r'<='
t_DEFINE = r':='
t_OPEN_ANGLE_BRACKET = r'<'
t_CLOSE_ANGLE_BRACKET = r'>'
t_OPEN_BRACE = r"{"
t_CLOSE_BRACE = r"}"
t_AT = r"@"
t_DOLLAR = r"\$"
t_COMMA = r","
#t_LEFT_SHIFT = r"<<"
#t_RIGHT_SHIFT = r">>"
#t_BITWISE_AND = r"&"
#t_BITWISE_OR = r"|"
#t_BITWISE_XOR = r"^"
t_LOGICAL_AND = r"&&"
t_LOGICAL_OR = r"\|\|"
t_LOGICAL_XOR = r"\^\^"
t_LOGICAL_IMPLICATION = r"->"
t_LOGICAL_BICONDITIONAL = r"<-->"
t_LOGICAL_EQUALITY = r"="
t_ATOM = r"'[\w]+"

precedence = (
     ('left', 'LOGICAL_IMPLICATION', 'LOGICAL_BICONDITIONAL'),
     ('left', 'LOGICAL_AND', 'LOGICAL_OR', 'LOGICAL_XOR'),
     ('left', 'LOGICAL_EQUALITY'),
     ('left', 'OPEN_PARENTHESIS'),
 )

reserved = {
    'bit': 'BIT',
    'bits': 'BITS',
    'boolean': 'BOOLEAN',
    'budget' : 'BUDGET',
    'byte' : 'BYTE',
    'case': 'CASE',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'enum': 'ENUM',
    'func': 'FUNC',
    'if' : 'IF',
    'int8': 'INT8',
    'interrupt': 'INTERRUPT',
    'loop': 'LOOP',
    'match': 'MATCH',
    'module' : 'MODULE',
    'nibble': 'NIBBLE',
    'pass': 'PASS',
    'record' : 'RECORD',
    'require' : 'REQUIRE',
    'while' : 'WHILE',
    'constraint': 'CONSTRAINT',
    'rules': 'RULES',
    'facts': 'FACTS',
}

tokens += list(reserved.values())

def t_NUMBER(t):
    # Supports
    # -       0xFF for hex
    # -      0o377 for octal
    # - 0b11111111 for binary
    # -        255 for decimal
    # also supports _ as a seperator
    r'(?P<hex>0x[0-9a-fA-F_]+)|(?P<bin>0b[01_]+)|(?P<oct>0o[0-7_]+)|(?P<dec>[\d_]+)'
    t.orig_value = t.value
    t.value = t.value.replace('_', '')

    v_hex = t.lexer.lexmatch.group('hex')
    v_dec = t.lexer.lexmatch.group('dec')
    v_bin = t.lexer.lexmatch.group('bin')
    v_oct = t.lexer.lexmatch.group('oct')

    v = t.value[2:]

    if v_dec:
        t.value = int(t.value)
    elif v_hex:
        t.value = int(v, 16)
    elif v_bin:
        t.value = int(v, 2)
    elif v_oct:
        t.value = int(v, 8)

    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_newline(t):
    r'[\r\n]+(?P<spaces>[\t\ ]*)'

    t.lexer.lineno += 1
    
    spaces = t.lexer.lexmatch.group('spaces')
    indent = 0
    if spaces is None:
       spaces = '' 
    indent = len(spaces)
    original_indent = 0
    if hasattr(t.lexer, 'indent'):
        original_indent = t.lexer.indent
    t.lexer.indent = indent
    t.value = indent

    if original_indent == indent:
        t.type = "NEWLINE"
    elif original_indent > indent:
        t.type = 'DEDENT'
    elif original_indent < indent:
        t.type = 'INDENT'

    return t

def t_WS(t):
    r'[\t\ ]+'
    pass

def t_COMMENT(t):
    r'\#.*'
    pass


def t_error(t):
    print("Illegal character '%s' (%d)" % (t.value[0], ord(t.value[0])))
    t.lexer.skip(1)

def K4Lexer():
    return lex.lex()

