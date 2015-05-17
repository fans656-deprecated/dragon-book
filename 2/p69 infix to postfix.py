# [69() - 92]
from __future__ import print_function

def expr():
    term()
    while True:
        if lookahead == '+':
            match('+')
            term()
            put('+')
        elif lookahead == '-':
            match('-')
            term()
            put('-')
        else:
            break

def term():
    if lookahead.isdigit():
        t = lookahead
        match(lookahead)
        put(t)
    else:
        raise Exception('syntax error: expecting digits')

def match(token):
    global lookahead
    if token == lookahead:
        try:
            lookahead = tokens.pop(0)
        except IndexError:
            lookahead = None
    else:
        raise Exception('syntax error: expecting {} instead of {}'.format(
            token, lookahead
            ))

def put(s):
    print(s, end=' ')

tokens = '''
3 + 5 - 4
'''.strip().split()
lookahead = tokens.pop(0)

expr()
print()
