# 2015-05-09 21:57:10
# generate random syntax tree based on an grammar
import string

from PySide.QtCore import *
from PySide.QtGui import *

from grammar import Grammar, Terminal, Nonterminal
from layout import layout

print 'Press any key to generate a new syntax tree'

# TODO
# limit the depth of syntax tree
# by select more "specific" derivation
# once reach a certain depth
# so the below EXPR grammar can be visualized
# (currently cause a maximum recursion exceed)

#<expr> -> <expr> + <term> | <expr> - <term>
#<term> -> <term> * <prim> | <term> / <prim>
#<prim> -> <digit>
#<digit> -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

grammar = Grammar('''
<list> -> <list> + <digit> | <list> - <digit> | <digit>
<digit> -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
''')

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.derive()

    def derive(self):
        self.syntaxTree = grammar.derive()
        self.update()

    def keyPressEvent(self, ev):
        ch = ev.text()
        if ch and ch in string.printable:
            self.derive()
        else:
            super(Widget, self).keyPressEvent(ev)

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        margin = self.width() / 10.0
        availWidth = self.width() - margin * 2
        availHeight = self.height() - margin * 2
        # layout
        tree = self.syntaxTree.clone()
        layout(tree)
        # calc extent
        xs, ys = zip(*((t.x, t.y) for t in tree))
        minX, maxX = min(xs), max(xs)
        minY, maxY = min(ys), max(ys)
        dx, dy = float(maxX - minX), float(maxY - minY)
        # scale
        for node in tree:
            pen = painter.pen()
            pen.setWidthF(0.2)
            painter.setPen(pen)
            node.x = margin + availWidth * ((node.x - minX) / dx if dx else 0.5)
            node.y = margin + availHeight * ((node.y - minY) / dy if dy else 0.5)
        # draw lines
        for node in tree:
            for c in node.children:
                painter.drawLine(node.x, node.y, c.x, c.y)
        # draw nonterminals
        painter.setFont(QFont('Courier New', 8))
        pen = painter.pen()
        pen.setBrush(QBrush(QColor(120,120,120)))
        painter.setPen(pen)
        for node in filter(lambda t: isinstance(t.data, Nonterminal), tree):
            painter.drawText(node.x - margin, node.y - margin, 2 * margin, 2 * margin,
                    Qt.AlignCenter, str(node.data))
        # draw terminals
        painter.setFont(QFont('Courier New', 14, QFont.Bold))
        pen = painter.pen()
        pen.setBrush(QBrush(QColor(0,0,0)))
        painter.setPen(pen)
        for node in filter(lambda t: isinstance(t.data, Terminal), tree):
            painter.drawText(node.x - margin, node.y - margin, 2 * margin, 2 * margin,
                    Qt.AlignCenter, str(node.data))

app = QApplication([])
w = Widget()
w.resize(640, 640)
w.show()
app.exec_()
