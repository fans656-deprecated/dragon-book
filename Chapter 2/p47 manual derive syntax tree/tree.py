from collections import defaultdict

class Tree(object):

    def __init__(self, data, children=[]):
        self.data = data
        self.children = children

    def width(self):
        return 0

    def layout(self):
        slots = defaultdict(lambda: 0)
        def setup(root, depth):
            root.y = depth
            n = len(root.children)
            if n:
                for c in root.children:
                    setup(c, depth + 1)
                beg = root.children[0].x
                end = root.children[-1].x
                root.x = (beg + end) / 2.0
            else:
                root.x = slots[depth] + root.width()
            dx = max(0, slots[depth] - root.x)
            root.offset = dx
            root.x += dx
            slots[depth] = root.x + root.width() + 1

        def offset(root, dx):
            root.x += dx
            print '{:20} {:5} {:5}'.format(root.data, root.x, root.y)
            for c in root.children:
                offset(c, dx + root.offset)

        setup(self, 0)
        offset(self, 0)

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

testTree = Tree('4444')
t = Tree('999999999')
t.children = [Tree('333'), Tree('333')]
testTree.children = [Tree('1'), t, Tree('1'), Tree('1')]

#testTree = Tree('1')
#testTree.children = [Tree('1'), Tree('999999999')]

if __name__ == '__main__':
    testTree.layout()
    #for t in testTree:
    #    print t.data
