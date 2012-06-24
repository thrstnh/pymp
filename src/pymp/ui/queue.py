from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .search import SearchBar
from ..logger import init_logger
from ..model.table import MyTableModel, myQTableView
from ..style import iconset
from ..config import init_env

logger = init_logger()
PYMPENV = init_env()


class QueueDialog(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        self.searchBar = SearchBar(self, iconset['delete'],
                                   PYMPENV['SEARCH_TIMEOUT'])
        self.tbl = myQTableView(self)
        self.model = MyTableModel(self)
        self.tbl.setModel(self.model)
        self.tbl.set_model(self.model)
        self.tbl.setShowGrid(False)
        vh = self.tbl.verticalHeader()
        vh.setVisible(False)
        vh.setDefaultSectionSize(14)
        hh = self.tbl.horizontalHeader()
        hh.setStretchLastSection(True)

        vbox.addWidget(self.searchBar)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.tbl, 1)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout(self)
        ok = QPushButton(QIcon(iconset['ok']), "", self)
        ok.clicked.connect(self.onOk)
        cancel = QPushButton(QIcon(iconset['cancel']), "", self)
        cancel.clicked.connect(self.onCancel)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        vbox.addLayout(hbox)
        layout = QFrame(self)
        layout.setLayout(vbox)
        self.setCentralWidget(layout)
        self.setWindowTitle('Queue Dialog')
        self.resize(800, 320)

    def append(self, item):
        logger.info("queue append to model")
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.model.append_(item)
        self.emit(SIGNAL("layoutChanged()"))

    def onOk(self):
        ''' exit dialog with ok'''
        logger.info("ok")
        self.setVisible(False)

    def onCancel(self):
        ''' exit dialog with cancel '''
        logger.info("cancel")
        self.setVisible(False)
