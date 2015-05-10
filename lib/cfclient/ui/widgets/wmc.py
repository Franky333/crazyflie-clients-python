__author__ = 'Markus Klein'

from PyQt4 import QtGui, QtCore

class WMCBlobDisplay(QtGui.QWidget):

    def __init__(self):
        super(WMCBlobDisplay, self).__init__()

        self.blob0 = QtCore.QPoint(100, 100)
        self.blob1 = QtCore.QPoint(200, 100)
        self.blob2 = QtCore.QPoint(100, 200)
        self.blob3 = QtCore.QPoint(200, 200)

        self.left = -1
        self.center = -1
        self.right = -1
        self.front = -1

        self.setMinimumSize(30, 30)

    def paintEvent(self, e):
        height = self.height()
        width = self.width()

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(0, 0, width, height, QtGui.QColor(0, 0, 0))

        painter.setPen(QtGui.QColor(255, 255, 255))
        if self.blob0 is not None:
            painter.drawLine(self.blob0.x() - 10, self.blob0.y(), self.blob0.x() + 10, self.blob0.y())
            painter.drawLine(self.blob0.x(), self.blob0.y() - 10, self.blob0.x(), self.blob0.y() + 10)

        if self.blob1 is not None:
            painter.drawLine(self.blob1.x() - 10, self.blob1.y(), self.blob1.x() + 10, self.blob1.y())
            painter.drawLine(self.blob1.x(), self.blob1.y() - 10, self.blob1.x(), self.blob1.y() + 10)

        if self.blob2 is not None:
            painter.drawLine(self.blob2.x() - 10, self.blob2.y(), self.blob2.x() + 10, self.blob2.y())
            painter.drawLine(self.blob2.x(), self.blob2.y() - 10, self.blob2.x(), self.blob2.y() + 10)

        if self.blob3 is not None:
            painter.drawLine(self.blob3.x() - 10, self.blob3.y(), self.blob3.x() + 10, self.blob3.y())
            painter.drawLine(self.blob3.x(), self.blob3.y() - 10, self.blob3.x(), self.blob3.y() + 10)
        painter.end()
