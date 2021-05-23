from parse import Node, result
from table import table, functions


temp_reg_values = {}
tree = result
TAC_table = {'main': []}
j = 0
if_count = 0
line_count = 0


def check_number(string):
    try:
        float(string)
        if string.isnumeric():
            return False
        return True
    except ValueError:
        return False


def check_scope(tree, name):
    if name.startswith('if') or (tree.isnumeric()) or (check_number(tree)):
        return True
    if tree in table.keys():
        if table[tree][2] == name:
            return True
        else:
            print('Scope error!')
            print(tree + ' ' + name)
            return False
    else:
        print('Incorrect variable ' + tree + ' ' + name)
        return False


def TAC_Search(tree):
    global line_count
    if len(tree.parts) == 3:
        GenerateTAC(tree.parts[0], 'main')
        GenerateTAC(tree.parts[2], 'main')
        for funct in tree.parts[1].parts:
            TAC_table[funct.type] = []
            GenerateTAC(funct, funct.type)
    else:
        GenerateTAC(tree.parts[0], 'main')
        GenerateTAC(tree.parts[1], 'main')
    TAC_table['main'].append('GOTO END')


def TAC_Func_Search(tree, name):
    global line_count
    if type(tree) != Node:
        return
    elif tree.type == 'Declaration':
        for i in tree.parts[0].parts:
            TAC_table[name].append('Declaration ' + i)
            line_count = line_count + 1
    elif tree.type == 'Assign':
        TAC_Assign(tree, name)
        TAC_table[name].append('-> ' + 't' + str(j - 1) + ' ' + tree.parts[0])

        line_count = line_count + 1
    else:
        for i in range(len(tree.parts)):
            TAC_Func_Search(tree.parts[i], name)


def GenerateTAC(tree, name):
    global j, if_count, line_count
    if type(tree) != Node and (tree == 'break' or tree == 'continue'):
        TAC_table[name].append(tree)
    elif type(tree) != Node:
        return
    elif tree.type == 'Declaration':
        for i in tree.parts[0].parts:
            TAC_table[name].append('Declaration ' + i)
            line_count = line_count + 1
    elif tree.type == 'Assign':
        if type(tree.parts[0]) == str and type(tree.parts[1]) == str:
            if not check_scope(tree.parts[0], name):
                return
            TAC_table[name].append('-> ' + tree.parts[1] + ' ' + tree.parts[0])
            line_count = line_count + 1
        else:
            TAC_Assign(tree, name)
            if not check_scope(tree.parts[0], name):
                return
            TAC_table[name].append('-> ' + 't' + str(j - 1) + ' ' + tree.parts[0])

            temp_reg_values['t' + str(j - 1)] = []
            temp_reg_values['t' + str(j - 1)].append(tree.parts[0])
            line_count = line_count + 1
            j = 0

    elif tree.type == 'if':
        TAC_Expr_Search(tree.parts[0], name)
        if_name = 'if' + str(if_count)
        if_count = if_count + 1
        TAC_table[if_name] = []
        TAC_table[name].append('IF ' + 't' + str(j - 1) + ' GOTO ' + if_name)
        GenerateTAC(tree.parts[1], if_name)
        TAC_table[if_name].append('GOTO after_if')
        line_count = line_count + 1
    elif tree.type == 'while':
        TAC_Expr_Search(tree.parts[0], name)
        if_name = 'if' + str(if_count)
        if_count = if_count + 1
        TAC_table[if_name] = []
        TAC_table[name].append('IF ' + 't' + str(j - 1) + ' GOTO ' + if_name)
        GenerateTAC(tree.parts[1], if_name)
        TAC_table[if_name].append('GOTO start_if')
        line_count = line_count + 1
    elif tree.type == 'return':
        if name == 'main':
            print('Error! Incorrect return location')
        else:
            TAC_Assign(tree.parts[0], name)
            TAC_table[name].append('return ' + 't' + str(j - 1))
    elif tree.type == 'print':
        TAC_table[name].append('print ' + tree.parts[0])

    else:
        for i in range(len(tree.parts)):
            GenerateTAC(tree.parts[i], name)


def TAC_Assign(tree, name):
    global j, line_count

    if type(tree) != Node:
        if not check_scope(tree, name):
            return
        return tree
    elif tree.type == '*' or tree.type == '/' or tree.type == '+' or tree.type == '-':
        operand = tree.type
        arg1 = TAC_Assign(tree.parts[0], name)
        arg2 = TAC_Assign(tree.parts[1], name)
        if arg1 is None and arg2 is None:
            arg1 = 't' + str(j - 2)
            temp_reg_values['t' + str(j - 2)] = []

            temp_reg_values['t' + str(j - 1)] = []
            temp_reg_values['t' + str(j - 2)].append('t' + str(j - 1))
            temp_reg_values['t' + str(j - 1)].append('t' + str(j - 2))
        if arg1 is None:
            arg1 = 't' + str(j - 1)
            temp_reg_values['t' + str(j - 1)] = []
            temp_reg_values['t' + str(j - 1)].append(arg2)
        if arg2 is None:
            arg2 = 't' + str(j - 1)
            temp_reg_values['t' + str(j - 1)].append(arg1)
        else:
            temp_reg_values['t' + str(j)] = []
            temp_reg_values['t' + str(j)].append(arg1)
        temp = 't' + str(j)
        j = j + 1
        TAC_table[name].append(str(operand) + ' ' + str(arg1) + ' ' + str(arg2) + ' ' + str(temp))
        line_count = line_count + 1
    elif tree.type in functions:
        string = 'Call ' + tree.type + ' '
        for arg in tree.parts[0].parts:
            string = string + arg + ' '
        temp = 't' + str(j)
        j = j + 1
        string = string + temp
        TAC_table[name].append(string)

    else:
        for i in range(len(tree.parts)):
            TAC_Assign(tree.parts[i], name)


def TAC_Expr_Search(tree, name):
    global j, line_count
    if type(tree) != Node:
        if not check_scope(tree, name):
            return
        return tree
    elif tree.type == 'and' or tree.type == 'or':
        operand = tree.type
        arg1 = TAC_Expr_Search(tree.parts[0], name)
        arg2 = TAC_Expr_Search(tree.parts[1], name)
        if arg1 is None and arg2 is None:
            arg1 = 't' + str(j - 2)
            arg2 = 't' + str(j - 1)

        if arg1 is None:
            arg1 = 't' + str(j - 1)
            temp_reg_values['t' + str(j - 1)].append(arg2)
        if arg2 is None:
            arg2 = 't' + str(j - 1)
            temp_reg_values['t' + str(j - 1)].append(arg1)
        temp = 't' + str(j)
        if not (temp in temp_reg_values):
            temp_reg_values[temp] = []
            temp_reg_values['t' + str(j)].append(arg1)
        j = j + 1
        print('op = ' + operand)
        print('arg1=' + str(arg1))
        print('arg2=' + str(arg2))
        print('temp=' + str(temp))
        TAC_table[name].append(str(operand) + ' ' + str(arg1) + ' ' + str(arg2) + ' ' + str(temp))
        line_count = line_count + 1
    elif tree.type == 'not':
        operand = tree.type
        TAC_Expr_Search(tree.parts[0], name)
        arg = 't' + str(j - 1)
        temp = 't' + str(j)
        j = j + 1
        TAC_table[name].append(str(operand) + ' ' + str(arg) + ' ' + str(temp))
        line_count = line_count + 1
    elif tree.type == '>' or tree.type == '<' or tree.type == '=':
        operand = tree.type
        arg1 = TAC_Assign(tree.parts[0], name)
        arg2 = TAC_Assign(tree.parts[1], name)
        temp = 't' + str(j)

        temp_reg_values[temp] = []
        temp_reg_values[temp].append(arg1)
        j = j + 1
        TAC_table[name].append(str(operand) + ' ' + str(arg1) + ' ' + str(arg2) + ' ' + str(temp))
        line_count = line_count + 1
    else:
        for i in range(len(tree.parts)):
            TAC_Expr_Search(tree.parts[i], name)


TAC_Search(tree)
for key in TAC_table:
    print(key + ' : ')
    for i in TAC_table[key]:
        print('\t' + str(i))
