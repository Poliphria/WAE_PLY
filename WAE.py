from WAEParser import parser
from copy import deepcopy


def eval_expression(tree):
    if tree[0] == 'num':
        return tree[1]
    elif tree[0] == 'id':
        return 'ERROR'
    elif tree[0] == '+' or tree[0] == '-' or tree[0] == '*' or tree[0] == '/':
        v1 = eval_expression(tree[1])
        if v1 == 'ERROR':
            return 'ERROR'
        v2 = eval_expression(tree[2])
        if v2 == 'ERROR':
            return 'ERROR'
        if tree[0] == '+':
            return v1 + v2
        elif tree[0] == '-':
            return v1 - v2
        elif tree[0] == '*':
            return v1 * v2
        elif v2 != 0:
            return v1 / v2
        else:
            return 'ERROR'
    elif tree[0] == 'if':  # if clause
        v1 = eval_expression(tree[1])
        if v1 == 'ERROR':
            return 'ERROR'
        if v1 != 0:
            return eval_expression(tree[2])
        else:
            return eval_expression(tree[3])
    else:
        newTree = deepcopy(tree[2])
        for value in tree[1]:
            val = eval_expression(value[1])
            if val == 'ERROR':
                return 'ERROR'
            var = value[0]
            if var == 'ERROR':
                return 'ERROR'
            newTree = substitute(var, val, newTree)
        return eval_expression(newTree)


def substitute(var, val, tree):
    if tree[0] == 'num':
        return ['num', tree[1]]
    elif tree[0] == 'id':
        if tree[1] == var:
            return ['num', val]
        else:
            newString = tree[1][:]
            return ['id', newString]
    elif tree[0] == '+' or tree[0] == '-' or tree[0] == '*' or tree[0] == '/':
        t1 = substitute(var, val, tree[1])
        t2 = substitute(var, val, tree[2])
        newOp = tree[0][:]
        return [newOp, t1, t2]
    elif tree[0] == 'if':
        t1 = substitute(var, val, tree[1])
        t2 = substitute(var, val, tree[2])
        t3 = substitute(var, val, tree[3])
        return ['if', t1, t2, t3]
    else:
        dontSub = False
        for value in tree[1]:
            if value[0] == var:
                dontSub = True
                break
        if not dontSub:
            t2 = substitute(var, val, tree[2])
        else:
            t2 = tree[2]
        return [tree[0][:], tree[1], t2]


def checkMultVar(tree):
    if tree[0] == 'num':
        return True
    elif tree[0] == 'id':
        return True
    elif tree[0] == '+' or tree[0] == '-' or tree[0] == '*' or tree[0] == '/':
        v1 = checkMultVar(tree[1])
        if v1 == False:
            return False
        v2 = checkMultVar(tree[2])
        if v2 == False:
            return False
        return True
    elif tree[0] == 'if':  # if clause
        v1 = checkMultVar(tree[1])
        if v1 == False:
            return False
        v2 = checkMultVar(tree[2])
        if v2 == False:
            return False
        v3 = checkMultVar(tree[3])
        if v3 == False:
            return False
        return True
    else:
        newTree = deepcopy(tree[2])
        listOfVars = []
        for value in tree[1]:
            listOfVars.append(value[0])

        for var in listOfVars:
            if listOfVars.count(var) > 1:
                return False
        return True


def read_input():
    result = ''
    while True:
        data = input('WAE: ').strip()
        if ';' in data:
            i = data.index(';')
            result += data[0:i + 1]
            break
        else:
            result += data + ' '
    return result


def main():
    while True:
        data = read_input()
        if data == 'exit;':
            break
        try:
            tree = parser.parse(data)
        except Exception as inst:
            print(inst.args[0])
            continue
        print(tree)
        if not checkMultVar(tree):
            print('Semantic Error!!!')
            return
        try:
            answer = eval_expression(tree)
            if answer == 'ERROR':
                print('\nEVALUATION ERROR\n')
            else:
                print('\nThe value is ' + str(answer) + '\n')
        except:
            pass


main()
