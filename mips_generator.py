from table import table
from TAC import check_number, TAC_table, temp_reg_values

floatReg = {}

data = ''
if_count = 0
skip_count = 0
flag = False
str_count = 0


def CreateRegTable():
    for i in range(len(temp_reg_values)):
        if temp_reg_values['t' + str(i)][0].isnumeric():
            temp_reg_values['t' + str(i)] = []
            temp_reg_values['t' + str(i)] = 'int'
            table['t' + str(i)] = []
            table['t' + str(i)] = 'int'
        elif check_number(temp_reg_values['t' + str(i)][0]):
            temp_reg_values['t' + str(i)] = []
            temp_reg_values['t' + str(i)] = 'real'
            floatReg['f' + str(i)] = []
            floatReg['f' + str(i)].append('real')
            table['t' + str(i)] = []
            table['t' + str(i)] = 'real'
        elif temp_reg_values['t' + str(i)][0] in table and table[temp_reg_values['t' + str(i)][0]][1] == 'int':

            temp_reg_values['t' + str(i)] = []
            temp_reg_values['t' + str(i)] = 'int'
            table['t' + str(i)] = []
            table['t' + str(i)] = 'int'
        elif temp_reg_values['t' + str(i)][0] in table and table[temp_reg_values['t' + str(i)][0]][1] == 'real':
            temp_reg_values['t' + str(i)] = []
            temp_reg_values['t' + str(i)] = 'real'
            floatReg['f' + str(i)] = []
            floatReg['f' + str(i)].append('real')
            table['t' + str(i)] = []
            table['t' + str(i)] = 'real'


def AssignHandler(f, parsed_commands):
    global data
    if parsed_commands[1].isnumeric() and (
            table[parsed_commands[2]][1] == 'int' or temp_reg_values[parsed_commands[2]][0] == 'i'):
        if parsed_commands[2] in temp_reg_values.keys() and temp_reg_values[parsed_commands[2]][0] != \
                parsed_commands[2]:
            f.write('\tli $' + parsed_commands[2] + ', ' + parsed_commands[1] + '\n')
        else:
            f.write('\tli $' + table[parsed_commands[2]][0] + ', ' + parsed_commands[1] + '\n')
    elif check_number(parsed_commands[1]) and (
            table[parsed_commands[2]][1] == 'real' or temp_reg_values[parsed_commands[2]][0] == 'r'):
        data = data + '\tdrob' + parsed_commands[1] + ': .float ' + parsed_commands[1] + '\n'
        if parsed_commands[2] in temp_reg_values.keys() and temp_reg_values[parsed_commands[2]][0] != \
                parsed_commands[2]:
            f.write('\tla $' + parsed_commands[2] + ', drob' + parsed_commands[1] + '\n')
        else:
            f.write('\tla $' + table[parsed_commands[2]][0] + ', drob' + parsed_commands[1] + '\n')
    elif parsed_commands[1].startswith('\"') and parsed_commands[1].endswith('\"') and (
            table[parsed_commands[2]][1] == 'str'):
        data = data + '\t' + parsed_commands[2] + ': .asciiz ' + parsed_commands[1] + '\n'

    elif parsed_commands[1] in table.keys():
        if parsed_commands[1] in temp_reg_values.keys() and temp_reg_values[parsed_commands[1]][0] != \
                parsed_commands[1]:
            if parsed_commands[2] in temp_reg_values.keys() and temp_reg_values[parsed_commands[2]][0] != \
                    parsed_commands[2]:
                if temp_reg_values[parsed_commands[1]][0] == 'r':

                    f.write('\tmov.s $f' + parsed_commands[2][1:] + ', $f' + parsed_commands[1][1:] + '\n')
                else:
                    f.write('\tmove $' + parsed_commands[2] + ', $f' + parsed_commands[1] + '\n')
            elif parsed_commands[2] in table.keys():
                if temp_reg_values[parsed_commands[1]][0] == 'r':

                    f.write(
                        '\tmov.s $' + table[parsed_commands[2]][0] + ', $f' + parsed_commands[1][1:] + '\n')
                else:
                    f.write('\tmove $' + table[parsed_commands[2]][0] + ', $' + parsed_commands[1] + '\n')
        elif parsed_commands[1] in table.keys():
            if parsed_commands[2] in table.keys():
                if table[parsed_commands[2]][1] == 'real':
                    f.write(
                        '\tmov.s $' + table[parsed_commands[2]][0] + ', $' + table[parsed_commands[1]][
                            0] + '\n')
                else:
                    f.write('\tmove $' + table[parsed_commands[2]][0] + ', $' + table[parsed_commands[1]][
                        0] + '\n')

    else:
        if parsed_commands[2] in table.keys():
            f.write('\tmove $' + parsed_commands[2] + ', $' + parsed_commands[1] + '\n')
        elif parsed_commands[2] in table.keys():
            f.write('\tmove $' + table[parsed_commands[2]][0] + ', $' + parsed_commands[1] + '\n')
        else:
            f.write('\tmove $' + parsed_commands[2] + ', $' + parsed_commands[1] + '\n')


def MultHandler(f, parsed_commands, table):
    if not (check_number(parsed_commands[1]) or check_number(parsed_commands[2])):
        if (parsed_commands[1].isnumeric() or table[parsed_commands[1]][1] == 'int' or
            temp_reg_values[parsed_commands[1]][
                0] == 'i') and (
                parsed_commands[2].isnumeric() or table[parsed_commands[2]][1] == 'int' or
                temp_reg_values[parsed_commands[2]][0] == 'i'):

            if parsed_commands[1].isnumeric():
                f.write('\tli $t0, ' + parsed_commands[1] + '\n')
                arg1 = '$t0'
                if parsed_commands[2].isnumeric():
                    f.write('\tli $t1, ' + parsed_commands[2] + '\n')
                    arg2 = '$t1'
                    f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'int':
                    arg2 = '$' + table[parsed_commands[2]][0]
                    f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                elif temp_reg_values[parsed_commands[2]][0] == 'i':
                    arg2 = '$' + parsed_commands[2]
                    f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
            elif (parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int') or (
                    temp_reg_values[parsed_commands[1]][0] == 'i' and parsed_commands[
                1] in temp_reg_values):
                if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int':
                    arg1 = '$' + table[parsed_commands[1]][0]
                else:
                    arg1 = '$' + parsed_commands[1]
                if parsed_commands[2].isnumeric():
                    f.write('\tli $t1, ' + parsed_commands[2] + '\n')
                    arg2 = '$t1'
                    f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'int':
                    arg2 = '$' + table[parsed_commands[2]][0]
                    f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                elif temp_reg_values[parsed_commands[2]][0] == 'i' and parsed_commands[
                    2] in temp_reg_values:
                    arg2 = '$' + parsed_commands[2]
                    f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')

                f.write('\tmflo $' + parsed_commands[3] + '\n')
        elif (parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real') or (
                temp_reg_values[parsed_commands[1]][0] == 'r' and parsed_commands[1] in temp_reg_values):
            if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real':
                arg1 = '$' + table[parsed_commands[1]][0]
            else:
                chislo = parsed_commands[1][1:]
                arg1 = '$f' + str(chislo)
            if check_number(parsed_commands[2]):
                f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
                arg2 = '$f1'
                f.write('\tmul.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real':
                arg2 = '$' + table[parsed_commands[2]][0]
                chislo = parsed_commands[3][1:]
                f.write('\tmul.s $f' + str(chislo) + ', ' + arg1 + ', ' + arg2 + '\n')
            elif temp_reg_values[parsed_commands[2]][0] == 'r' and parsed_commands[2] in temp_reg_values:
                chislo = parsed_commands[2][1:]
                arg2 = '$f' + str(chislo)
                f.write('\tmul.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
            else:
                print('Incorrect type!')
                return
    elif check_number(parsed_commands[1]):

        f.write('\tli.s $f0, ' + parsed_commands[1] + '\n')
        arg1 = '$f0'
        if check_number(parsed_commands[2]):
            f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
            arg2 = '$f1'
            f.write('\tmul.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real':
            arg2 = '$' + table[parsed_commands[2]][0]
            f.write('\tmul.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif temp_reg_values[parsed_commands[2]][0] == 'r' and parsed_commands[2] in temp_reg_values:
            chislo = parsed_commands[2][1:]
            arg2 = '$f' + str(chislo)
            f.write('\tmul.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        else:
            print('Incorrect type!')
            return


def DivHandler(f, parsed_commands, table):
    if not (check_number(parsed_commands[1]) or check_number(parsed_commands[2])):
        if (parsed_commands[1].isnumeric() or table[parsed_commands[1]][1] == 'int' or
            temp_reg_values[parsed_commands[1]][
                0] == 'i') and (
                parsed_commands[2].isnumeric() or table[parsed_commands[2]][1] == 'int' or
                temp_reg_values[parsed_commands[1]][0] == 'i'):
            if parsed_commands[1].isnumeric():
                f.write('\tli $t0, ' + parsed_commands[1] + '\n')
                arg1 = '$t0'
                if parsed_commands[2].isnumeric():
                    f.write('\tli $t1, ' + parsed_commands[2] + '\n')
                    arg2 = '$t1'
                    f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'int':
                    arg2 = '$' + table[parsed_commands[2]][0]
                    f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                elif temp_reg_values[parsed_commands[2]][0] == 'i':
                    arg2 = '$' + parsed_commands[2]
                    f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
            elif (parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int') or (
                    temp_reg_values[parsed_commands[1]][0] == 'i' and parsed_commands[
                1] in temp_reg_values):
                if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int':
                    arg1 = '$' + table[parsed_commands[1]][0]
                else:
                    arg1 = '$' + parsed_commands[1]
                if parsed_commands[2].isnumeric():
                    f.write('\tli $t1, ' + parsed_commands[2] + '\n')
                    arg2 = '$t1'
                    f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'int':
                    arg2 = '$' + table[parsed_commands[2]][0]
                    f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                elif temp_reg_values[parsed_commands[2]][0] == 'i' and parsed_commands[
                    2] in temp_reg_values:
                    arg2 = '$' + parsed_commands[2]
                    f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
            f.write('\tmflo $' + parsed_commands[3] + '\n')
        elif ((parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real') or (
                temp_reg_values[parsed_commands[1]][0] == 'r' and parsed_commands[1] in temp_reg_values)):
            if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real':
                arg1 = '$' + table[parsed_commands[1]][0]
            else:
                arg1 = '$f' + parsed_commands[1][1:]
            if check_number(parsed_commands[2]):
                f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
                arg2 = '$f1'
                f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real':
                arg2 = '$' + table[parsed_commands[2]][0]
                f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif temp_reg_values[parsed_commands[2]][0] == 'r' and parsed_commands[2] in temp_reg_values:
                arg2 = '$f' + parsed_commands[2][1:]
                f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')

        else:
            print('Incorrect type!')
            return

    elif check_number(parsed_commands[1]):

        f.write('\tli.s $f0, ' + parsed_commands[1] + '\n')
        arg1 = '$f0'
        if check_number(parsed_commands[2]):
            f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
            arg2 = '$f1'
            f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real':
            arg2 = '$' + table[parsed_commands[2]][0]
            f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif temp_reg_values[parsed_commands[2]][0] == 'r' and parsed_commands[2] in temp_reg_values:
            arg2 = '$f' + parsed_commands[2][1:]
            f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        else:
            print('Incorrect type!')
            return
    elif (parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real') or (
            temp_reg_values[parsed_commands[1]][0] == 'r' and parsed_commands[1] in temp_reg_values):
        if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real':
            arg1 = '$' + table[parsed_commands[1]][0]
        else:
            arg1 = '$f' + parsed_commands[1][1:]
        if check_number(parsed_commands[2]):
            f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
            arg2 = '$f1'
            f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real':
            arg2 = '$' + table[parsed_commands[2]][0]
            f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif temp_reg_values[parsed_commands[2]][0] == 'r' and parsed_commands[2] in temp_reg_values:
            arg2 = '$f' + parsed_commands[2][1:]
            f.write('\tdiv.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')

    else:
        print('Incorrect type!')
        return


def PlusHandler(f, parsed_commands, table):
    if not (check_number(parsed_commands[1]) or check_number(parsed_commands[2])):
        if (parsed_commands[1].isnumeric() or table[parsed_commands[1]][1] == 'int' or
            temp_reg_values[parsed_commands[1]][
                0] == 'i') and (
                parsed_commands[2].isnumeric() or table[parsed_commands[2]][1] == 'int' or
                temp_reg_values[parsed_commands[2]][0] == 'i'):
            if parsed_commands[1].isnumeric():
                f.write('\tli $t0, ' + parsed_commands[1] + '\n')
                arg1 = '$t0'
                if parsed_commands[2].isnumeric():
                    f.write('\tli $t1, ' + parsed_commands[2] + '\n')
                    arg2 = '$t1'
                    f.write('\taddu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'int':
                    arg2 = '$' + table[parsed_commands[2]][0]
                    f.write('\taddu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif temp_reg_values[parsed_commands[2]][0] == 'i':
                    arg2 = '$' + parsed_commands[2]
                    f.write('\taddu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif (parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int') or (
                    temp_reg_values[parsed_commands[1]][0] == 'i' and parsed_commands[
                1] in temp_reg_values):
                if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int':
                    arg1 = '$' + table[parsed_commands[1]][0]
                else:
                    arg1 = '$' + parsed_commands[1]
                if parsed_commands[2].isnumeric():
                    f.write('\tli $t1, ' + parsed_commands[2] + '\n')
                    arg2 = '$t1'
                    f.write('\taddu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'int':
                    arg2 = '$' + table[parsed_commands[2]][0]
                    f.write('\taddu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif temp_reg_values[parsed_commands[2]][0] == 'i' and parsed_commands[
                    2] in temp_reg_values:
                    arg2 = '$' + parsed_commands[2]
                    f.write('\taddu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif ((parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real') or (
                temp_reg_values[parsed_commands[1]][0] == 'r' and parsed_commands[1] in temp_reg_values)):
            if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real':
                arg1 = '$' + table[parsed_commands[1]][0]
            else:
                arg1 = '$f' + parsed_commands[1][1:]
            if check_number(parsed_commands[2]):
                f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
                arg2 = '$f1'
                f.write('\taddu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real':
                arg2 = '$' + table[parsed_commands[2]][0]
                f.write('\taddu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif temp_reg_values[parsed_commands[2]][0] == 'r' and parsed_commands[2] in temp_reg_values:
                arg2 = '$f' + parsed_commands[2][1:]
                f.write('\taddu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')

        else:
            print('Incorrect type!')
            return

    elif check_number(parsed_commands[1]):

        f.write('\tli.s $f0, ' + parsed_commands[1] + '\n')
        arg1 = '$f0'
        if check_number(parsed_commands[2]):
            f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
            arg2 = '$f1'
            f.write('\taddu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif (parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real') or (
                temp_reg_values[parsed_commands[1]][0] == 'r' and parsed_commands[1] in temp_reg_values):
            if parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real':
                arg2 = '$' + table[parsed_commands[2]][0]
            elif temp_reg_values[parsed_commands[1]][0] == 'r' and parsed_commands[1] in temp_reg_values:
                arg2 = '$' + parsed_commands[2]
            f.write('\taddu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        else:
            print('Incorrect type!')
            return
    else:
        print('Incorrect type!')
        return


def MinusHandler(f, parsed_commands, table):
    if not (check_number(parsed_commands[1]) or check_number(parsed_commands[2])):
        if (parsed_commands[1].isnumeric() or table[parsed_commands[1]][1] == 'int' or
            temp_reg_values[parsed_commands[1]][
                0] == 'i') and (
                parsed_commands[2].isnumeric() or table[parsed_commands[2]][1] == 'int' or
                temp_reg_values[parsed_commands[1]][0] == 'i'):
            if parsed_commands[1].isnumeric():
                f.write('\tli $t0, ' + parsed_commands[1] + '\n')
                arg1 = '$t0'
                if parsed_commands[2].isnumeric():
                    f.write('\tli $t1, ' + parsed_commands[2] + '\n')
                    arg2 = '$t1'
                    f.write('\tsubu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'int':
                    arg2 = '$' + table[parsed_commands[2]][0]
                    f.write('\tsubu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif temp_reg_values[parsed_commands[2]][0] == 'i':
                    arg2 = '$' + parsed_commands[2]
                    f.write('\tsubu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif (parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int') or (
                    temp_reg_values[parsed_commands[1]][0] == 'i' and parsed_commands[
                1] in temp_reg_values):
                if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int':
                    arg1 = '$' + table[parsed_commands[1]][0]
                else:
                    arg1 = '$' + parsed_commands[1]
                if parsed_commands[2].isnumeric():
                    f.write('\tli $t1, ' + parsed_commands[2] + '\n')
                    arg2 = '$t1'
                    f.write('\tsubu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'int':
                    arg2 = '$' + table[parsed_commands[2]][0]
                    f.write('\tsubu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif temp_reg_values[parsed_commands[2]][0] == 'i' and parsed_commands[
                    2] in temp_reg_values:
                    arg2 = '$' + parsed_commands[2]
                    f.write('\tsubu $' + parsed_commands[3] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif ((parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real') or (
                temp_reg_values[parsed_commands[1]][0] == 'r' and parsed_commands[1] in temp_reg_values)):
            if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real':
                arg1 = '$' + table[parsed_commands[1]][0]
            else:
                arg1 = '$f' + parsed_commands[1][1:]
            if check_number(parsed_commands[2]):
                f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
                arg2 = '$f1'
                f.write('\tsubu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real':
                arg2 = '$' + table[parsed_commands[2]][0]
                f.write('\tsubu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
            elif temp_reg_values[parsed_commands[2]][0] == 'r' and parsed_commands[2] in temp_reg_values:
                arg2 = '$f' + parsed_commands[2][1:]
                f.write('\tsubu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        else:
            print('Incorrect Type!')
            return

    elif check_number(parsed_commands[1]):

        f.write('\tli.s $f0, ' + parsed_commands[1] + '\n')
        arg1 = '$f0'
        if check_number(parsed_commands[2]):
            f.write('\tli.s $f1, ' + parsed_commands[2] + '\n')
            arg2 = '$f1'
            f.write('\tsubu.s $f' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        elif (parsed_commands[2] in table and table[parsed_commands[2]][1] == 'real') or (
                temp_reg_values[parsed_commands[2]][0] == 'r' and parsed_commands[2] in temp_reg_values):
            if parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real':
                arg2 = '$' + table[parsed_commands[2]][0]
            else:
                arg2 = '$f' + parsed_commands[2][1:]
            f.write('\tsubu.s $' + parsed_commands[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
        else:
            print('Incorrect Type!')
            return
    else:
        print('Incorrect Type!')
        return


def LogicHandler(f, parsed_commands):
    if parsed_commands[0] == 'and' or parsed_commands[0] == 'or':
        f.write('\t' + parsed_commands[0] + ' $' + parsed_commands[3] + ', $' + parsed_commands[1] + ', $' +
                parsed_commands[
                    2] + '\n')


def NotHandler(f, parsed_commands):
    index = parsed_commands[2][1:]
    index = int(index) + 1
    temp = 't' + str(index)
    f.write('\tla $' + temp + ' false\n')
    f.write('\tnor $' + parsed_commands[2] + ', $' + parsed_commands[1] + ', $' + temp + '\n')


def GOTOHandler(f, parsed_commands):
    if parsed_commands[1] == 'after_if':
        print('after false')
        f.write('\tj L' + str(if_count - 1) + '\n')
    elif parsed_commands[1] == 'start_if':
        f.write('\tj L' + str(if_count - 2) + '\n')
    else:
        f.write('\tj ' + parsed_commands[1] + '\n')


def BreakHandler(f):
    f.write('\tj L' + str(if_count - 3) + '\n')


def ContinueHandler(f, tac):
    for label in tac:
        f.write(label + ':\n')
        for command in tac[label]:
            parsed_commands = command.split(' ')
            if parsed_commands[0] == 'continue':
                f.write('\tj L' + str(if_count - 4) + '\n')


def PrintHanlder(f, parsed_commands, table, data, str_count):
    if parsed_commands[0] == 'print':
        if parsed_commands[1].startswith('\"') and parsed_commands[1].endswith('\"'):
            data = data + '\tstr' + str(str_count) + ': .asciiz ' + parsed_commands[1] + '\n'
            str_count = str_count + 1
            f.write('\tli $v0, 4\n')
            f.write('\tla $a0, ' + 'str' + str(str_count - 1) + '\n')
            f.write('\tsyscall\n')
        elif parsed_commands[1] in table and table[parsed_commands[1]][1] == 'str':
            f.write('\tli $v0, 4\n')
            f.write('\tla $a0, ' + parsed_commands[1] + '\n')
            f.write('\tsyscall\n')
        elif parsed_commands[1].isnumeric():
            f.write('\tli $v0, 1\n')
            f.write('\tla $a0, ' + parsed_commands[1] + '\n')
            f.write('\tsyscall\n')
        elif check_number(parsed_commands[1]):
            data = data + '\tdrob' + parsed_commands[1] + ': .float ' + parsed_commands[1] + '\n'
            f.write('\tli $v0, 2\n')
            f.write('\tlwc1 $f12, drob' + parsed_commands[1] + '\n')
            f.write('\tsyscall\n')
        elif parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int':
            f.write('\tli $v0, 1\n')
            f.write('\tla $a0, ' + '($' + table[parsed_commands[1]][0] + ')\n')
            f.write('\tsyscall\n')
        elif parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real':
            f.write('\tli $v0, 2\n')
            f.write('\tlwc1 $f12, ($' + table[parsed_commands[1]][0] + ')\n')
            f.write('\tsyscall\n')


def ReturnHanlder(f, tac):
    for label in tac:
        f.write(label + ':\n')
        for command in tac[label]:
            parsed_commands = command.split(' ')
            if parsed_commands[0] == 'return':
                f.write('\tmove $t9, $' + parsed_commands[1] + '\n')
                f.write('\tjr $ra\n')


def CallHandler(f, tac, table):
    for label in tac:
        f.write(label + ':\n')
        for command in tac[label]:
            parsed_commands = command.split(' ')
            if parsed_commands[0] == 'Call':
                args = parsed_commands[2:len(parsed_commands) - 1]
                for i in range(len(args)):
                    f.write('\tmove $a' + str(i) + ', $' + table[args[i]][0] + '\n')
                f.write('\tjal ' + parsed_commands[1] + '\n')
                f.write('\tmove $' + parsed_commands[len(parsed_commands) - 1] + ', $t9\n')


def Generate(tac, table):
    global if_count, skip_count, flag, str_count, data
    data = data + '.data\n\ttrue: .byte 1\n\tfalse: .byte 0\n'
    f = open('../examples/MIPS.s', 'w')
    f.write('.text\n')

    for reg in table:
        if reg == 't0':
            break
        temp_reg_values[reg] = []
        temp_reg_values[reg].append(reg)

    for label in tac:
        f.write(label + ':\n')
        for command in tac[label]:
            parsed_commands = command.split(' ')
            if parsed_commands[0] == '->':
                AssignHandler(f, parsed_commands)
            elif parsed_commands[0] == '*':
                MultHandler(f, parsed_commands, table)
            elif parsed_commands[0] == '/':
                DivHandler(f, parsed_commands, table)
            elif parsed_commands[0] == '+':
                PlusHandler(f, parsed_commands, table)
            elif parsed_commands[0] == '-':
                MultHandler(f, parsed_commands, table)
            elif (parsed_commands[0] == '<' or parsed_commands[0] == '>'
                  or parsed_commands[0] == '='):
                if not flag:
                    L = 'L' + str(if_count)
                    if_count = if_count + 1
                    flag = True
                    f.write(L + ':\n')
                if parsed_commands[0] == '<':
                    f.write('\tla $' + parsed_commands[3] + ', false\n')
                    f.write('\tbge $' + table[parsed_commands[1]][0] + ', $' + table[parsed_commands[2]][
                        0] + ', SKIP' + str(
                        skip_count) + '\n')
                    f.write('\tla $' + parsed_commands[3] + ', true\n')
                    f.write('SKIP' + str(skip_count) + ':\n')
                    skip_count = skip_count + 1
                elif parsed_commands[0] == '>':
                    f.write('\tla $' + parsed_commands[3] + ', false\n')
                    f.write('\tble $' + table[parsed_commands[1]][0] + ', $' + table[parsed_commands[2]][
                        0] + ', SKIP' + str(
                        skip_count) + '\n')
                    f.write('\tla $' + parsed_commands[3] + ', true\n')
                    f.write('SKIP' + str(skip_count) + ':\n')
                    skip_count = skip_count + 1
                elif parsed_commands[0] == '=':
                    f.write('\tla $' + parsed_commands[3] + ', false\n')
                    f.write('\tbne $' + table[parsed_commands[1]][0] + ', $' + table[parsed_commands[2]][
                        0] + ', SKIP' + str(
                        skip_count) + '\n')
                    f.write('\tla $' + parsed_commands[3] + ', true\n')
                    f.write('SKIP' + str(skip_count) + ':\n')
                    skip_count = skip_count + 1

            elif parsed_commands[0] == 'and' or parsed_commands[0] == 'or':
                LogicHandler(f, parsed_commands)
            elif parsed_commands[0] == 'not':
                NotHandler(f, parsed_commands)
            elif parsed_commands[0] == 'IF':
                flag = False
                index = parsed_commands[1][1:]
                index = int(index) + 1
                temp = 't' + str(index)
                f.write('\tla $' + temp + ', true\n')
                f.write('\tbeq $' + temp + ', $' + parsed_commands[1] + ', ' + parsed_commands[3] + '\n')
                f.write('L' + str(if_count) + ':\n')
                if_count = if_count + 1
            elif parsed_commands[0] == 'GOTO':
                GOTOHandler(f, parsed_commands)
            elif parsed_commands[0] == 'break':
                f.write('\tj L' + str(if_count - 3) + '\n')
            elif parsed_commands[0] == 'continue':
                f.write('\tj L' + str(if_count - 4) + '\n')
            elif parsed_commands[0] == 'print':
                if parsed_commands[0] == 'print':
                    if parsed_commands[1].startswith('\"') and parsed_commands[1].endswith('\"'):
                        data = data + '\tstr' + str(str_count) + ': .asciiz ' + parsed_commands[1] + '\n'
                        str_count = str_count + 1
                        f.write('\tli $v0, 4\n')
                        f.write('\tla $a0, ' + 'str' + str(str_count - 1) + '\n')
                        f.write('\tsyscall\n')
                    elif parsed_commands[1] in table and table[parsed_commands[1]][1] == 'str':
                        f.write('\tli $v0, 4\n')
                        f.write('\tla $a0, ' + parsed_commands[1] + '\n')
                        f.write('\tsyscall\n')
                    elif parsed_commands[1].isnumeric():
                        f.write('\tli $v0, 1\n')
                        f.write('\tla $a0, ' + parsed_commands[1] + '\n')
                        f.write('\tsyscall\n')
                    elif check_number(parsed_commands[1]):
                        data = data + '\tdrob' + parsed_commands[1] + ': .float ' + parsed_commands[1] + '\n'
                        f.write('\tli $v0, 2\n')
                        f.write('\tlwc1 $f12, drob' + parsed_commands[1] + '\n')
                        f.write('\tsyscall\n')
                    elif parsed_commands[1] in table and table[parsed_commands[1]][1] == 'int':
                        f.write('\tli $v0, 1\n')
                        f.write('\tla $a0, ' + '($' + table[parsed_commands[1]][0] + ')\n')
                        f.write('\tsyscall\n')
                    elif parsed_commands[1] in table and table[parsed_commands[1]][1] == 'real':
                        f.write('\tli $v0, 2\n')
                        f.write('\tlwc1 $f12, ($' + table[parsed_commands[1]][0] + ')\n')
                        f.write('\tsyscall\n')

            elif parsed_commands[0] == 'return':
                f.write('\tmove $t9, $' + parsed_commands[1] + '\n')
                f.write('\tjr $ra\n')
            elif parsed_commands[0] == 'Call':
                args = parsed_commands[2:len(parsed_commands) - 1]
                for i in range(len(args)):
                    f.write('\tmove $a' + str(i) + ', $' + table[args[i]][0] + '\n')
                f.write('\tjal ' + parsed_commands[1] + '\n')
                f.write('\tmove $' + parsed_commands[len(parsed_commands) - 1] + ', $t9\n')

    f.write('END:\n')
    f.write(data)
    f.close()


CreateRegTable()
Generate(TAC_table, table)
