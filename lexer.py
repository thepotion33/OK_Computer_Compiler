from ply import lex
import re

reserved = {
    'function': 'FUNCTION',
    'return': 'RETURN',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'write': 'WRITE',
    'while': 'WHILE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'int': 'INT',
    'real': 'REAL',
    'str': 'STRING',
    'variables': 'VARIABLES'
}

tokens = [
    'EQUAL', 'TYPE', 'COMA', 'OPENBRACKET', 'CLOSEBRACKET', 'OPEN', 'CLOSE', 'ASSIGN',
    'SEMICOLON', 'SUM', 'SUB', 'MUL', 'DIV', 'MORE', 'LESS', 'NUMBER_INT', 'NUMBER_FLOAT', 'ID',
]

tokens += reserved.values()

t_TYPE = r'\-->'
t_EQUAL = r'\='
t_OPENBRACKET = r'\('
t_CLOSEBRACKET = r'\)'
t_COMA = r'\,'
t_OPEN = r'\{'
t_CLOSE = r'\}'
t_ASSIGN = r'\->'
t_SEMICOLON = r'\;'
t_SUM = r'\+'
t_SUB = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_MORE = r'\>'
t_LESS = r'\<'
t_NUMBER_INT = r'\d+'
t_NUMBER_FLOAT = r'\d+\.\d+'
t_STRING = r'\"(\\.|[^$"])+"'


def t_comment(t):
    r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    pass


def t_ID(t):
    r'[a-z]\w*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)


t_ignore = ' \r\t\f'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex(reflags=re.UNICODE | re.DOTALL | re.IGNORECASE)


class Lexer:
    def __init__(self, program):
        self.program = program

    @staticmethod
    def run(program):
        lexer = lex.lex(reflags=re.UNICODE | re.DOTALL | re.IGNORECASE)
        lexer.input(program)
        while True:
            token = lexer.token()
            if not token: break
            print(token)
