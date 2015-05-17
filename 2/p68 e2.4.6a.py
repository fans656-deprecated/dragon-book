def S():
    if lookahead == 'a':
        match('a')
    elif lookahead == '+':
        match('+')
        S()
        S()
    elif lookahead == '-':
        match('-')
        S()
        S()
    else:
        raise Exception('syntax error: unexpected {}'.format(lookahead))

def match(token):
    global lookahead
    if lookahead == token:
        print 'match {}'.format(lookahead)
        try:
            lookahead = tokens.pop(0)
        except IndexError:
            lookahead = None
    else:
        raise Exception('syntax error: expecting {}, got {}'.format(
            token, lookahead
            ))

tokens = '''
+ - a a a
'''.strip().split()

lookahead = tokens.pop(0)

S()
if tokens:
    raise Exception('syntax error: trailing program {}'.format(
        ' '.join(tokens)))
