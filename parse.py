import ply.yacc as yacc
from lexer import tokens


class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts


def p_Program(p):
    '''Program : VARIABLES declaration_list OPEN stmt_list CLOSE
            | VARIABLES declaration_list function_list OPEN stmt_list CLOSE'''
    if len(p) == 6:
        p[0] = Node('Program', [p[2], p[4]])
    else:
        p[0] = Node('Program', [p[2], p[3], p[5]])


def p_function_list(p):
    '''function_list : function
               | function_list SEMICOLON function'''
    if len(p) == 2:
        p[0] = Node('Function', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_function(p):
    '''function : FUNCTION ID OPENBRACKET declaration_list CLOSEBRACKET OPEN stmt_list_def CLOSE
            | FUNCTION ID OPENBRACKET declaration_list CLOSEBRACKET OPEN VARIABLES declaration_list stmt_list_def CLOSE'''
    if len(p) == 9:
        p[0] = Node(p[2], [p[4], p[7]])
    else:
        p[0] = Node(p[2], [p[4], p[8], p[9]])


def p_defstmt(p):
    '''defstmt : ID OPENBRACKET args CLOSEBRACKET'''
    p[0] = Node(p[1], [p[3]])


def p_args(p):
    '''args : arg
            | args SEMICOLON arg'''
    if len(p) == 2:
        p[0] = Node('args', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_arg(p):
    '''arg : ID
            | NUMBER_INT
            | NUMBER_FLOAT
            | OPENBRACKET exp CLOSEBRACKET'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_declaration_list(p):
    '''declaration_list : declaration
               | declaration_list SEMICOLON declaration'''
    if len(p) == 2:
        p[0] = Node('Variables', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_declaration(p):
    '''declaration : id_list TYPE type'''
    p[0] = Node('Declaration', [p[1], p[3]])


def p_type(p):
    '''type : INT
            | REAL'''
    p[0] = Node('Type', [p[1]])


def p_id_list(p):
    '''id_list : ID
                | id_list COMA ID'''
    if len(p) == 2:
        p[0] = Node('ID', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_stmt_list(p):
    '''stmt_list : statement
                | stmt_list SEMICOLON statement'''
    if len(p) == 2:
        p[0] = Node("Statement's list", [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_stmt(p):
    '''statement : assign
            | write
            | while
            | if'''
    if len(p) == 2:
        p[0] = p[1]


def p_stmt_list_if(p):
    '''stmt_list_if : stmt_if
                | stmt_list_if SEMICOLON stmt_if'''
    if len(p) == 2:
        p[0] = Node('Condition', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_stmt_list_def(p):
    '''stmt_list_def : stmt_def
                | stmt_list_def SEMICOLON stmt_def'''
    if len(p) == 2:
        p[0] = Node('Conditional statement', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_stmt_if(p):
    '''stmt_if : assign
            | write
            | while
            | if
            | CONTINUE
            | BREAK'''
    if len(p) == 2:
        p[0] = p[1]


def p_stmt_def(p):
    '''stmt_def : assign
            | write
            | while
            | if
            | return'''
    if len(p) == 2:
        p[0] = p[1]


def p_return(p):
    '''return : RETURN exp'''
    p[0] = Node(p[1], [p[2]])


def p_assign(p):
    '''assign : ID ASSIGN exp'''
    p[0] = Node('Assign', [p[1], p[3]])


def p_exp(p):
    '''exp : term
            | exp SUM term
            | exp SUB term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_while(p):
    '''while : WHILE bool_exp OPEN stmt_list CLOSE'''
    p[0] = Node('while', [p[2], p[4]])


def p_term(p):
    '''term : factor
            | term MUL factor
            | term DIV factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_factor(p):
    '''factor : defstmt
            | ID
            | NUMBER_INT
            | NUMBER_FLOAT
            | OPENBRACKET exp CLOSEBRACKET'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_print(p):
    '''write : WRITE OPENBRACKET exp CLOSEBRACKET
                | WRITE OPENBRACKET STRING CLOSEBRACKET'''
    p[0] = Node('print', [p[3]])


def p_if(p):
    '''if : IF bool_exp THEN OPEN stmt_list_if CLOSE ELSE OPEN stmt_list_if CLOSE
            | IF bool_exp THEN OPEN stmt_list_if CLOSE'''
    if len(p) == 11:
        p[0] = Node('if', [p[2], p[5], p[9]])
    else:
        p[0] = Node('if', [p[2], p[5]])


def p_bool_exp(p):
    '''bool_exp : bool_exp OR bool_exp_term
                | bool_exp_term
                | NOT bool_exp
                | bool'''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])
    else:
        p[0] = p[1]


def p_bool_exp_term(p):
    '''bool_exp_term : bool_exp_term AND bool
                | bool'''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])
    else:
        p[0] = p[1]


def p_bool(p):
    '''bool : OPENBRACKET exp EQUAL exp CLOSEBRACKET
            | OPENBRACKET exp MORE exp CLOSEBRACKET
            | OPENBRACKET exp LESS exp CLOSEBRACKET'''
    p[0] = Node(p[3], [p[2], p[4]])


def p_error(p):
    print('Unexpected token:', p)


file = open('testcode3.ok', 'r')
program = file.read()
parser = yacc.yacc()
result = parser.parse(program)
print(result)
