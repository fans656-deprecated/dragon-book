import copy

from PySide.QtCore import *
from PySide.QtGui import *

import tree

tree.Tree.width = lambda self: len(str(self.data)) / 2.0

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.tree = tree.testTree
        self.tree.layout()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        def getExtent(nodes, getVal, getOffset):
            def reducer(acc, node):
                mi, ma = acc
                val = getVal(node)
                nmi, nma = val, val
                if nmi < mi: mi = nmi
                if nma > ma: ma = nma
                return (mi, ma)

            init = (getVal(nodes[0]), getVal(nodes[0]))
            return reduce(reducer, nodes, init)

        tree = copy.deepcopy(self.tree)
        nodes = list(tree)
        minX, maxX = getExtent(nodes, lambda t: t.x, lambda t: t.width())
        minY, maxY = getExtent(nodes, lambda t: t.y, lambda t: 0)
        dx, dy = maxX - minX, maxY - minY

        margin = self.width() / 20.0
        availWidth = self.width() - margin * 2
        availHeight = self.height() - margin * 2

        for node in nodes:
            node.x = margin + availWidth * ((node.x - minX) / float(dx) if dx else 0.5)
            node.y = margin + availHeight * ((node.y - minY) / float(dy) if dy else 0.5)
        for node in nodes:
            for c in node.children:
                painter.drawLine(node.x, node.y, c.x, c.y)
        painter.setBrush(QBrush(QColor(255,255,255)))
        painter.setFont(QFont('Courier New', 14))
        fm = QFontMetrics(painter.font())
        for node in nodes:
            text = str(node.data)
            rc = fm.boundingRect(text)
            bx, by = 5, 3
            rc.adjust(-bx, -by, bx, by)
            rc.moveTo(node.x - rc.width() / 2.0, node.y - rc.height() / 2.0)
            painter.drawRect(rc)
            painter.drawText(rc, Qt.AlignCenter, str(node.data))
            #painter.drawEllipse(QPointF(node.x, node.y), 10, 10)

app = QApplication([])
w = Widget()
w.resize(640, 640)
w.show()
app.exec_()
