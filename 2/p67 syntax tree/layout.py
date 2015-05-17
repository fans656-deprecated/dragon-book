from collections import defaultdict
import itertools

def layout(root, depth=0):
    def setup(root, depth, slots=defaultdict(lambda: 0)):
        if root:
            root.y = depth
            n = len(root.children)
            if n:
                for c in root.children:
                    setup(c, depth + 1, slots)
                root.x = sum(c.x for c in root.children) / float(n)
            else:
                root.x = slots[depth]
            dx = max(slots[depth] - root.x, 0)
            root.x += dx
            root.offset = dx
            slots[depth] = root.x + 1

    def offset(root, dx):
        if root:
            root.x += dx
            for c in root.children:
                offset(c, dx + root.offset)

    setup(root, depth)
    offset(root, 0)
