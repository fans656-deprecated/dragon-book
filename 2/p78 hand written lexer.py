# 2015-05-17 17:07:43
# [78() - 101]
class EOF(Exception):

    pass

def nextchar():
    global peek
    try:
        peek = text.pop(0)
    except IndexError:
        peek = ''

def eatspace():
    global line
    while True:
        if peek and peek in ' \t':
            pass
        elif peek == '\n':
            line += 1
        else:
            break
        nextchar()

def getToken():
    eatspace()
    if not peek:
        raise EOF('EOF')
    if peek.isalpha():
        return ident()
    elif peek.isdigit():
        return number()
    elif peek == '=':
        nextchar()
        return ('=', )
    elif peek == '+':
        nextchar()
        return ('+', )
    elif peek == '-':
        nextchar()
        return ('-', )
    elif peek == ';':
        nextchar()
        return (';', )
    else:
        raise Exception('Unknown character at line {}: {}({})'.format(
            line, peek, ord(peek)
            ))

def ident():
    lexme = ''
    while peek.isalnum() or peek == '_':
        lexme += peek
        nextchar()
    if lexme not in words:
        words[lexme] = ('id', lexme)
    return words[lexme]

def number():
    val = 0
    while peek.isdigit():
        val = val * 10 + int(peek)
        nextchar()
    return ('num', val)

words = {
        'for': ('for',),
        'if': ('if',),
        'then': ('then',),
        'while': ('while',),
        }
text = list('''
if a then count = count + increment;
''')

line = 1
peek = None

try:
    nextchar()
    while True:
        print getToken()
except EOF:
    pass
