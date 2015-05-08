# 2015-05-08 21:11:43
# extract terminals & nonterminals from a grammar
from itertools import chain

data = '''
<list> -> <list> + <digit> | <list> - <digit> | <digit>
<digit> -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
'''

def split(s, sep=' '):
    return map(str.strip, s.split(sep))

def production(line):
    left, right = split(line, '->')
    right = split(right, '|')
    return left, right

def splitRight(bodys):
    itemsLists = map(split, bodys)
    return list(chain(*itemsLists))

def rightItems(rights):
    return list(chain(*map(splitRight, rights)))

lines = filter(bool, split(data, '\n'))
productions = map(production, lines)
start = productions[0][0]
nonterminals, terminals = zip(*productions)
nonterminals = set(nonterminals)
terminals = set(rightItems(terminals)) - nonterminals

fmt = '    {}'
print 'Nonterminals:'
for nt in nonterminals:
    print fmt.format(nt)
print

print 'Terminals:'
for t in terminals:
    print fmt.format(t)
print

print 'Start nonterminal:'
print fmt.format(start)
