import random
import operator
import pymp.sqldb
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ..config import TABLE_OPTIONS
from ..logger import init_logger

logger = init_logger()

__all__ = ['myQTableView', 'MyTableModel']


class myQTableView(QTableView):

    def keyPressEvent(self, event):
        print "myQTableView.keyPressEvent"
        self.key = QString()
        if event.key() == Qt.Key_Up:
            self.key = "up"
        elif event.key() == Qt.Key_Down:
            self.key = "down"
        elif event.key() == Qt.Key_Space:
            self.key = "space"
        elif event.key() == Qt.Key_Enter:
            self.key == "enter"
        elif Qt.Key_A <= event.key() <= Qt.Key_Z:
#            if event.modifiers() & Qt.ControlModifier:
#                self.key = "CTRL+"
#                print "CTRL+",
            self.key += event.text()
            print event.text()

        if self.key:
            if self.key == 'enter':
                print "play"
            elif self.key == 'space':
                print "pause"
            elif self.key == 'up':
                print "up"
            elif self.key == 'down':
                print "down"
            elif self.key in ('j', 'J'):
                print "jump to search"
            elif self.key in ('b', 'B'):
                print "next"
            else:
                print "unhandled key: ", self.key
            self.key = QString(self.key)
            self.update()
        else:
            QWidget.keyPressEvent(self, event)


class MyTableModel(QAbstractTableModel):

    def __init__(self, parent=None, *args):
        self.arraydata = []
        self.headerkeys, self.headerdata = self._init_tbl_columns()
        QAbstractTableModel.__init__(self, parent, *args)

    def empty(self):
        return self.length() > 0

    def length(self):
        return len(self.arraydata)

    def shuffle(self):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        random.shuffle(self.arraydata)
        self.emit(SIGNAL("layoutChanged()"))

    def clear(self):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = []
        self.emit(SIGNAL("layoutChanged()"))

    def _init_tbl_columns(self):
        keys = []
        data = []
        for k,v in TABLE_OPTIONS.items():
            if v[0]:
                data.append((v[1], v[2]))
                keys.append((v[1], k))
        return ([k for (id,k) in sorted(keys)], [d for (id,d) in sorted(data)])

    def append(self, row):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata.append(row)
        self.emit(SIGNAL("layoutChanged()"))

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if self.arraydata:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def data_row(self, row):
        return self.arraydata[row]

    def data_at(self, row, col):
        return QVariant(self.arraydata[row][col])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, nCol, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(nCol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))
