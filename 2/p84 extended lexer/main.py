class EOF(Exception): pass
class SyntaxError(Exception): pass

def getChar():
    global peek, line, col
    try:
        peek = text.pop(0)
        if peek == '\n':
            line += 1
            col = 0
        else:
            col += 1
        return peek
    except IndexError:
        # so that eatSpace have the chance to read EOF which is previously
        # supressed by, say, identifier
        peek = ' '
        raise EOF()

def peekChar():
    try:
        return text[0]
    except IndexError:
        raise EOF()

def eatComment():
    try:
        ch = peekChar()
    except EOF:
        return False
    if ch == '/':
        try:
            while getChar() != '\n':
                continue
        except EOF:
            pass
        return True
    elif ch == '*':
        try:
            getChar()
            while True:
                if getChar() == '*':
                    if getChar() == '/':
                        return True
        except EOF:
            raise SyntaxError('Nonterminated comment')
    else:
        return False

def eatSpace():
    while True:
        if peek in '\t \n':
            pass
        elif peek == '/':
            # eatComment will consume just the comment
            # or if there is no comment, it returns with peek untouched
            if not eatComment():
                return
        else:
            return
        getChar()

def identifier():
    lexeme = peek
    try:
        while True:
            getChar()
            if peek.isalnum():
                lexeme += peek
            else:
                break
    except EOF:
        pass
    if lexeme not in words:
        words[lexeme] = ('id', lexeme)
    return words[lexeme]

def getInt():
    val = 0
    try:
        while True:
            val = val * 10 + int(peek)
            if not getChar().isdigit():
                break
    except EOF:
        pass
    return val

def getFractional(hasIntPart):
    val = 0
    base = 0.1
    try:
        while getChar().isdigit():
            val += int(peek) * base
            base /= 10
    except EOF:
        if not hasIntPart:
            raise
    return val

def number():
    if peek == '.':
        hasIntPart = False
        val = 0
    else:
        hasIntPart = True
        val = getInt()
    if peek == '.':
        fval = getFractional(hasIntPart)
        return ('float', val + fval)
    else:
        return ('int', val)

def lookForward(init, forward, accepted=True):
    ret = init
    try:
        if peekChar() == forward:
            getChar()
            ret += forward
            accepted = True
        getChar()
    except EOF:
        pass
    return (ret, ) if accepted else None

def getToken():
    eatSpace()
    if peek.isalpha():
        return identifier()
    elif peek.isdigit() or peek == '.':
        return number()
    elif peek in '+-*/;':
        ch = peek
        getChar()
        return (ch, )
    elif peek == '=':
        return lookForward('=', '=')
    elif peek == '<':
        return lookForward('<', '=')
    elif peek == '>':
        return lookForward('>', '=')
    elif peek == '!':
        ret = lookForward('!', '=', False)
        if ret:
            return ret
    raise SyntaxError('Unrecognized character: \'{}\'(\\{})'.format(
        peek, ord(peek)
        ))

#line, col = 1, 0
#peek = ' '
#words = {
#        'if': ('if', ),
#        'while': ('while', ),
#        'for': ('for', ),
#        'true': ('true', ),
#        'false': ('false'),
#        }
#text = list('''\
#<<=!=>>==
#''')
#try:
#    while True:
#        print getToken()
#except SyntaxError as e:
#    print 'Error at {}:{}: {}'.format(line, col, e)
#except EOF:
#    pass
#print '-- finished'
#exit()

import testcase
for desc, text in testcase.testcases:
    line, col = 1, 0
    peek = ' '
    words = {
            'if': ('if', ),
            'while': ('while', ),
            'for': ('for', ),
            'true': ('true', ),
            'false': ('false'),
            }
    text = list(text)
    print '-- start ({})'.format(desc)
    try:
        while True:
            print getToken()
    except SyntaxError as e:
        print 'Error at {}:{}: {}'.format(line, col, e)
    except EOF:
        pass
    print '-- finished'
    print
