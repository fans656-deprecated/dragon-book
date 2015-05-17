# 2015-05-09 16:48:12
# generate random syntax tree based on an grammar
from itertools import chain, groupby
from random import choice

def split(text, sep=' '):
    return tuple(s.strip() for s in text.split(sep))

class Nonterminal(object):

    def __init__(self, name, production=None):
        self.name = name
        self.production = production

    def __repr__(self):
        return self.name

    def derive(self):
        return choice(self.production.bodys)

class Terminal(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Production(object):

    def __init__(self, lookup, head, bodys):
        self.head = lookup[head]
        self.head.production = self
        self.bodys = [tuple(lookup[name] for name in body) for body in bodys]

class Grammar(object):

    def __init__(self, text):
        def mutiple(production):
            l, r = production
            return map(lambda body: (l, body), split(r, '|'))

        # flatten the grammar
        lines = filter(bool, split(text, '\n'))
        productions = list(chain(*(mutiple(split(l, '->')) for l in lines)))
        start = productions[0][0]
        productions = [(l, split(r, ' ')) for l, r in productions]
        productions = list(set(productions))
        # nonterminals & terminals
        nonterminals, terminals = map(set, zip(*productions))
        terminals = set(chain(*terminals)) - nonterminals
        makeLookup = lambda f, a: map(lambda t: (t, f(t)), a)
        lookup = dict(makeLookup(Nonterminal, nonterminals) + makeLookup(Terminal, terminals))
        # group back productions
        productions.sort(key=lambda t: t[0])
        productions = [Production(lookup, k, [r for _, r in g])
                for k, g in groupby(productions, key=lambda t: t[0])]
        # assign
        self.productions = productions
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.start = lookup[start]

    def derive(self):
        def derive_(root, depth=0):
            root.children = map(Tree, root.data.derive())
            isNontermial = lambda t: isinstance(t.data, Nonterminal)
            for c in filter(isNontermial, root.children):
                derive_(c, depth + 1)
            return root
        return derive_(Tree(self.start))

class Tree(object):

    def __init__(self, data, children=[]):
        self.data = data
        self.children = children

    def __str__(self, depth=0):
        s = '   ' * depth + str(self.data) + '\n'
        for c in self.children:
            s += c.__str__(depth + 1)
        return s

    def __iter__(self):
        def f(root):
            yield root
            for c in root.children:
                for r in f(c):
                    yield r
        return f(self)

    def clone(self):
        root = Tree(self.data)
        root.children = [c.clone() for c in self.children]
        return root

if __name__ == '__main__':
    #<list> -> <digit>
    s = '''
    <list> -> <list> + <digit> | <list> - <digit> | <digit>
    <digit> -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    '''
    g = Grammar(s)
    print g.derive()
