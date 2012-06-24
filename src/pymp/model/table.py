import random
import operator
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ..config import TABLE
from ..logger import init_logger

logger = init_logger()

__all__ = ['myQTableView', 'MyTableModel']


class myQTableView(QTableView):

    def __init__(self, parent=None, *args, **kw):
        QTableView.__init__(self, parent, *args, **kw)

    def set_model(self, model):
        self.model = model

    def _check_visible(self):
        for i, h in enumerate(self.model.header_hidden):
            self.setColumnHidden(i, not h)

    def _check_width(self):
        for i, w in enumerate(self.model.header_width):
            self.setColumnWidth(i, w)

    def append(self, item):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        ret = self.model.append_(item)
        self._check_visible()
        self._check_width()
        self.emit(SIGNAL("layoutChanged()"))
        return ret


class MyTableModel(QAbstractTableModel):

    def __init__(self, arraydata=None, header=None, parent=None, *args, **kw):
        QAbstractTableModel.__init__(self, parent, *args, **kw)
        self.arraydata = arraydata
        self.header = header
        self._populate()

    def _populate(self):
        self.arraydata = []
        order = operator.itemgetter(2)
        stable = sorted(TABLE, key=order)
        self.header_names = self._extract(3, stable)
        self.header_keys = self._extract(0, stable)
        self.header_hidden = self._extract(1, stable)
        self.header_width = self._extract(4, stable)

    def _extract(self, key, table):
        return [item[key] for item in table]

    def rowCount(self, parent):
        return len(self.arraydata)

    def empty_(self):
        return self.rowCount(None) > 0

    def set_data_(self, arr):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = arr
        self.emit(SIGNAL("layoutChanged()"))

    def clear_(self):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = []
        self.emit(SIGNAL("layoutChanged()"))

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()

        return QVariant(self.arraydata[index.row()][index.column()])

    def row_id_(self, data):
        for idx, item in enumerate(self.arraydata):
            if item[0] == data[0]:
                return idx
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_names[col])
        return QVariant()

    def sort(self, Ncol, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata,
                            key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def append_(self, row):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata.append(row)
        self.emit(SIGNAL("layoutChanged()"))

    def shuffle_(self):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        random.shuffle(self.arraydata)
        self.emit(SIGNAL("layoutChanged()"))

    def data_row_(self, row):
        return self.arraydata[row]
