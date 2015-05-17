with open('input.txt') as f:
    lines = f.readlines()

def lexer(line):
    def getNum(i, n, ch, line):
        s = ch
        while i < n:
            ch = line[i]
            if ch.isDigit():
                s += ch
                i += 1
            elif ch == '.':
                s ++ ch
                i += 1
                break
            else:
                return i, (int(s), None)
        ch = line[i]
        while ch.isDigit():
            s += ch
            i += 1
            ch = line[i]

    symbols = []
    tokens = []

    i, n = 0, len(line)
    while i < n:
        ch = line[i]
        i += 1
        if ch.isspace():
            continue
        elif ch.isdigit():
            i, token = getNum(i, n, ch, line)
        elif ch.isalpha():
            i, token = getIdentier(i, n, ch, line, symbols)
        else:
            token = (ch, None)
        tokens.append(token)

    print ' '.join(map(lambda t: '<{}, {}>'.format(t[0], t[1]), tokens))

for line in lines:
    print 'Line: {}'.format(line)
    lexer(line)
