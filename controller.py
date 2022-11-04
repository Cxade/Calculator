import logger
import model


actions = {
    "^": lambda x, y: str(float(x) ** float(y)),
    "*": lambda x, y: str(float(x) * float(y)),
    "/": lambda x, y: str(float(x) / float(y)),
    "+": lambda x, y: str(float(x) + float(y)),
    "-": lambda x, y: str(float(x) - float(y)),
}

def spl(string):
    string = string.replace(' ', '').strip()
    string = string.replace('+', ' + ')\
        .replace('-', ' - ')\
        .replace('*', ' * ')\
        .replace('/', ' / ')\
        .replace('(', ' ( ')\
        .replace(')', ' ) ')
    string = string.split()
    return string


def scob(line):
    lst = []
    i = 0
    while i < len(line):
        if line[i] == '(':
            m = line.index(")", i)
            lst.append(line[i+1:m])
            i = m
        else:
            lst.append(line[i])
        i += 1
    return lst



def in_scob(lst):
    for i in range(len(lst)):
        if isinstance(lst[i], list):
            a, b, c = scob(lst[i])
            lst[i] = actions[b](a, c)
    return lst


def result(lst):
    st = ''
    prior = [i for i, j in enumerate(lst) if j in "*/"]
    while prior:
        t = prior[0]
        a, b, c = lst[t - 1: t + 2]
        lst.insert(t-1,actions[b](a, c))
        del lst[t: t + 3]
        prior = [i for i, j in enumerate(lst) if j in "*/"]
    while len(lst) > 1:
        a, b, c = lst[:3]
        del lst[:3]
        lst.insert(0, actions[b](a, c))  
    return st.join(lst)


def last():
    model.result_expres = result(in_scob(scob(spl(model.expres))))
    logger.logger(f'{model.expres} = {model.result_expres}') 