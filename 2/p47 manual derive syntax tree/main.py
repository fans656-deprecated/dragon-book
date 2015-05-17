import copy

from PySide.QtCore import *
from PySide.QtGui import *

from tree import Tree, testTree

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.tree = testTree

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        tree = copy.deepcopy(self.tree)
        borderX, borderY = 5, 3
        painter.setFont(QFont('Courier New', 14))
        fm = QFontMetrics(painter.font())
        Tree.boundingRect = lambda t: fm.boundingRect(str(t.data)).adjusted(
                -borderX, -borderY, borderX, borderY)
        minX, maxX, minY, maxY = tree.layout()
        dx, dy = maxX - minX, maxY - minY
        #print minX, maxX, minY, maxY, dx, dy

        margin = self.width() / 20.0
        availWidth = self.width() - margin * 2
        availHeight = self.height() - margin * 2
        #print availWidth, availHeight

        for node in tree:
            node.x = margin + availWidth * (node.x - minX) / float(dx)
            node.y = margin + availHeight * (node.y - minY) / float(dy)
            #print '{:10} {:5.2f} {:5.2f}'.format(node.data, node.x, node.y)
        for node in tree:
            for c in node.children:
                painter.drawLine(node.x, node.y, c.x, c.y)
        painter.setBrush(QBrush(QColor(255,255,255)))
        for node in tree:
            rc = node.boundingRect()
            rc.moveTo(node.x - rc.width() / 2.0, node.y - rc.height() / 2.0)
            painter.drawRect(rc)
            painter.drawText(rc, Qt.AlignCenter, str(node.data))
            #painter.drawEllipse(QPointF(node.x, node.y), 10, 10)

app = QApplication([])
w = Widget()
w.resize(640, 640)
w.show()
app.exec_()
