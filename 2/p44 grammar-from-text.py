# 2015-05-15 14:03:48
#
# for simplicity, we assume '->' and '|' is not used as symbols in
# the language
#
# non-terminals don't need special form as <foo>
# cause it's determined by it's position in the productions
# i.e. all head of productions forms the set of non-terminals
# (denoted as NT)
#
# furthermore, all symbols in the productions forms the set
# of terminals & non-terminals (denoted as S)
# so T = S - NT is the set of terminals
#
# productions can be implemented as bodys attached to non-terminals
# so in the future we can add methods like `derive`
# and then foo.derive where foo is a non-terminal
text = '''
list -> list + digit
list -> list - digit
list -> digit
digit -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
'''

#text = r'''
#call -> id ( opt-params )
#opt-params -> params | \epsilon
#params -> params , param | param
#'''

class Bunch(dict):

    def __init__(self, **kwargs):
        super(Bunch, self).__init__(kwargs)
        self.__dict__.update(kwargs)

class Symbol(object):

    def __init__(self, name):
        self.name = name

class Terminal(Symbol):

    def __init__(self, name):
        super(Terminal, self).__init__(name)

    def __repr__(self):
        return self.name

class Nonterminal(Symbol):

    def __init__(self, name):
        super(Nonterminal, self).__init__(name)
        self.bodys = []

    def __repr__(self):
        bodys = ' | '.join(' '.join(t.name for t in body)
                for body in self.bodys)
        return '{} -> {}'.format(self.name, bodys)

class Grammar(object):

    def __init__(self, text):
        ps = map(makeProduction, split(text, '\n'))
        nts = set(p.head for p in ps)
        ts = set(flatten(flatten(p.bodys for p in ps))) - nts
        nts = map(Nonterminal, nts)
        ts = map(Terminal, ts)
        lookup = {t.name: t for t in nts + ts}
        for p in ps:
            lookup[p.head].bodys += [[lookup[name] for name in body]
                    for body in p.bodys]
        self.nonterminals = nts
        self.terminals = ts
        self.start = lookup[ps[0].head]

def flatten(xss):
    return [x for xs in xss for x in xs]

def makeProduction(line):
    h, bs = split(line, '->')
    bs = [split(b, ' ') for b in split(bs, '|')]
    return Bunch(head=h, bodys=bs)

def split(s, sep):
    return filter(bool, (t.strip() for t in s.split(sep)))

if __name__ == '__main__':
    g = Grammar(text)

    print 'Text:'
    print text
    print

    print 'Nonterminals:'
    for nt in g.nonterminals:
        print '\t', nt

    print
    print 'Terminals:'
    for t in g.terminals:
        print '\t', t

    print
    print 'Start symbol:'
    print '\t', g.start
