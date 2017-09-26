__author__ = 'Markus Klein'

from PyQt5 import QtGui, QtCore


class WMCBlobDisplay(QtGui.QWidget):

    WMC_X_RES = 1023.0
    WMC_Y_RES = 767.0

    def __init__(self):
        super(WMCBlobDisplay, self).__init__()

        self.blobs = [None, None, None, None]

        self.left = -1
        self.center = -1
        self.right = -1
        self.front = -1

        self.setMinimumSize(30, 30)

    def setBlob(self, blobId, x, y):
        if blobId > 3 or blobId < 0:
            return
        self.blobs[blobId] = QtCore.QPoint(WMCBlobDisplay.WMC_Y_RES - y, WMCBlobDisplay.WMC_X_RES - x)
        self.repaint()

    def setTPattern(self, l, r, c, f):
        if l > 3 or l < 0 or r > 3 or r < 0 or c > 3 or c < 0 or f > 3 or f < 0:
            return

        self.left = l
        self.right = r
        self.center = c
        self.front = f
        self.repaint()

    def clearTPattern(self):
        self.left = -1
        self.right = -1
        self.center = -1
        self.front = -1
        self.repaint()


    def clearBlob(self, blobId):
        if blobId > 3 or blobId < 0:
            return
        self.blobs[blobId] = None
        self.repaint()

    def paintEvent(self, e):
        height = self.height()
        width = self.width()

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(0, 0, width, height, QtGui.QColor(0, 0, 0))

        if (self.left is not -1) and (self.blobs[0] is not None) and (self.blobs[1] is not None) and (self.blobs[2] is not None) and (self.blobs[3] is not None):
            left = self._scaleBlob(self.blobs[self.left])
            right = self._scaleBlob(self.blobs[self.right])
            center = self._scaleBlob(self.blobs[self.center])
            front = self._scaleBlob(self.blobs[self.front])

            painter.setPen(QtGui.QColor(0, 255, 0))
            painter.drawLine(left, center)

            painter.setPen(QtGui.QColor(255, 0, 0))
            painter.drawLine(center, right)

            painter.setPen(QtGui.QColor(0, 0, 255))
            painter.drawLine(center, front)

        painter.setPen(QtGui.QColor(255, 255, 255))
        for blob in self.blobs:
            if blob is not None:
                blob = self._scaleBlob(blob)
                painter.drawLine(blob.x() - 10, blob.y(), blob.x() + 10, blob.y())
                painter.drawLine(blob.x(), blob.y() - 10, blob.x(), blob.y() + 10)

        painter.end()

    def _scaleBlob(self, blob):
        return QtCore.QPoint((blob.x() / WMCBlobDisplay.WMC_Y_RES) * self.width(),
                             (blob.y() / WMCBlobDisplay.WMC_X_RES) * self.height())
