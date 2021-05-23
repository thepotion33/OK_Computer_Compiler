from parse import result, Node

table = []
functions = []


def DepthSearcher(result):
    if type(result) != Node:
        return
    elif result.type == 'Function':
        for j in result.parts:
            if len(j.parts) == 2:
                FuncDepthSearcher(j, j.type)
                functions.append(j.type)
            elif len(j.parts) == 3:
                functions.append(j.type)
                for l in j.parts:
                    FuncDepthSearcher(l, j.type)
    elif result.type == 'Declaration':
        for i in result.parts[0].parts:
            table.append((i, result.parts[1].parts[0], 'main'))
        return
    else:
        for i in range(len(result.parts)):
            DepthSearcher(result.parts[i])


def FuncDepthSearcher(result, function):
    if type(result) != Node:
        return
    elif result.type == 'Declaration':
        for i in result.parts[0].parts:
            table.append((i, result.parts[1].parts[0], function))
    else:
        for i in range(len(result.parts)):
            FuncDepthSearcher(result.parts[i], function)


def edit_table(table):
    new_table = {}
    index = 0
    new_table1 = {}
    scope = 'main'
    for i in table:
        new_table[i[0]] = []
        new_table[i[0]].append('s' + str(index))
        new_table[i[0]].append(i[1])
        new_table[i[0]].append(i[2])
        index = index + 1
    index = 0
    xy = 0

    for i in new_table:
        new_table1[i[0]] = []
        if new_table[i][2] != 'main':
            if scope != new_table[i][2]:
                xy = 0
            scope = new_table[i][2]
            new_table1[i[0]].append('a' + str(xy))
            xy = xy + 1
            new_table1[i[0]].append(new_table[i][1])
            new_table1[i[0]].append(new_table[i][2])
        else:
            new_table1[i[0]].append('s' + str(index))
            index = index + 1
            new_table1[i[0]].append(new_table[i][1])
            new_table1[i[0]].append(new_table[i][2])
    return new_table1


DepthSearcher(result)
table = edit_table(table)

for key in table:
    print(key + ' : ')
    print(table[key])
