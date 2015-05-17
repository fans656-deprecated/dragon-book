from collections import defaultdict

class Tree(object):

    def __init__(self, data, children=[]):
        self.data = data
        self.children = children

    def height(self):
        return self.boundingRect().height()

    def width(self):
        return self.boundingRect().width()

    def layout(self):
        slots = defaultdict(lambda: 0)
        def setup(root, depth):
            root.y = depth
            root.offset = 0
            n = len(root.children)
            if n:
                for c in root.children:
                    setup(c, depth + 1)
                beg = root.children[0].x
                end = root.children[-1].x
                root.x = (beg + end) / 2.0
                dx = max(0, slots[depth] - (root.x - root.width() / 2.0))
                root.offset += dx
                root.x += dx
            else:
                root.x = slots[depth] + root.width() / 2.0
            slots[depth] = root.x + root.width() / 2.0 + 1
            #print slots

        def offset(root, dx):
            root.x += dx
            #print '{:20} {:5} {:5}'.format(root.data, root.x, root.y)
            for c in root.children:
                offset(c, dx + root.offset)

        setup(self, 0)
        offset(self, 0)
        minX = min(t.x - t.width() / 2.0 for t in self)
        maxX = max(t.x + t.width() / 2.0 for t in self)
        minY = min(t.y for t in self)
        maxY = max(t.y for t in self)
        return minX, maxX, minY, maxY

    def __iter__(self):
        def f():
            yield self
            for c in self.children:
                for t in iter(c):
                    yield t
        return f()

    def __repr__(self, depth=0):
        s = '  ' * depth + repr(self.data)
        for c in self.children:
            s += '\n' + c.__repr__(depth + 1)
        return s

#testTree = Tree('list')
#t = Tree('welcome to US')
#t.children = [Tree('foo'), Tree('bar')]
#testTree.children = [Tree('digit'), t, Tree('+'), Tree('digit')]

testTree = Tree('1111')
t = Tree('333333333')
t.children = [Tree('666'), Tree('777')]
testTree.children = [Tree('2'), t, Tree('4'), Tree('5')]

#testTree = Tree('1')
#testTree.children = [Tree('1'), Tree('999999999')]

if __name__ == '__main__':
    testTree.layout()
    #for t in testTree:
    #    print t.data
