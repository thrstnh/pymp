import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .tageditor import ID3Edit
from ..logger import init_logger
from ..model.table import MyTableModel, myQTableView
from ..style import iconset

logger = init_logger()


class PlaylistPanel(QWidget):
    '''
        Playlist Table

        click
        dclick

    '''
    # send signal on double click
    playCurrent = pyqtSignal(QString)
    playNext = pyqtSignal(QString)
    enqueue = pyqtSignal(list)
    dequeue = pyqtSignal(list)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()
        # current tracks
        self.tracks = {}
        self.parent = parent

    def initUI(self):
        ''' TODO: init user interface '''
        self.tbl = myQTableView(self) #QTableView(self)
        self.model = MyTableModel()
        self.tbl.setModel(self.model)
        self.tbl.setShowGrid(False)
        self.tbl.setColumnHidden(0, True)
        self.tbl.setColumnHidden(self.model.column_length()-1, True)
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl.setSortingEnabled(True)
        self.tbl.setWordWrap(False)
        self.tbl.setAlternatingRowColors(True)
        self.tbl.setFocusPolicy(Qt.NoFocus)
        self.tbl.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl.customContextMenuRequested.connect(self.popup)
        #self.tbl.setRowHeight()
        self.tbl.resizeRowsToContents()
        vh = self.tbl.verticalHeader()
        vh.setVisible(False)
        vh.setDefaultSectionSize(14)
        hh = self.tbl.horizontalHeader()
        hh.setStretchLastSection(True)

        self.toolbar = QToolBar('Clear Playlist')
        ac = QAction(QIcon(iconset['clear']), "Clear Playlist", self)
        ac.setStatusTip("Clear Playlist")
        ac.triggered.connect(self.clearPlaylist)
        self.toolbar.addAction(ac)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.tbl, 1)
        hbox.addWidget(self.toolbar)

        #vbox = QVBoxLayout(self)

#        self.tbl.clicked.connect(self.clicked)
        self.tbl.doubleClicked.connect(self.double_clicked)
#        self.tbl.activated.connect(self.activated)
#        self.tbl.entered.connect(self.entered)
#        self.tbl.pressed.connect(self.pressed)

    def popup(self, point):
        idx = self.tbl.selectionModel().currentIndex()
        data = self.model.data_row(idx.row())

        menu = QMenu()
        id3Action = menu.addAction('ID3 Editor')
        queueAction = menu.addAction('Queue')
        enqueueAction = menu.addAction('enqueue track')
        dequeueAction = menu.addAction('dequeue track')
        action = menu.exec_(self.mapToGlobal(point))

        if action == id3Action:
            id3dlg = ID3Edit(self, data[-1])
            id3dlg.show()
        elif action == queueAction:
            self.parent.queuedlg.show()
        elif action == enqueueAction:
            logger.info('enqueue {}'.format(data))
            self.enqueue.emit(data)
        elif action == dequeueAction:
            self.dequeue.emit(data)
        else:
            logger.info('unknown action (QTableView)')

    def clearPlaylist(self):
        self.model.clear()

    def usePattern(self, pattern):
        tstart = time.time()
        if not pattern:
            [self.appendModel(item) for (k, item) in self.tracks.items()]
        else:
            pattern = str(pattern).lower().split()
            self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.model.clear()
            self.tbl.emit(SIGNAL("layoutChanged()"))
            for (k, v) in self.tracks.items():
                if self.__valid_entry(v, map(str.strip, pattern), (1, 2, 3)):
                    self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
                    self.appendModel(v)
                    self.tbl.emit(SIGNAL("layoutChanged()"))
                    continue

        self.parent.statusBar().showMessage('%s Tracks' % (self.model.row_length()))
        self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.tbl.resizeRowsToContents()
        self.tbl.emit(SIGNAL("layoutChanged()"))
        logger.info(':fill {}s'.format(time.time() - tstart))

    def __valid_entry(self, item, pattern=[], keys=[], case_sensitive=False):
        r'''example:
                item = ['Tenacious D', 'Tribute', 'Homemade', 'Rock']
                pattern = ['tenac', 'rock']
                keys = (0, 3)
                # would match every pattern in item with given index
        '''
        if not case_sensitive:
            item = [s.lower() if isinstance(s, basestring) else s for s in item]
            pattern = map(str.lower, pattern)
        # mode: or
        mor = True if 'or' in pattern else False
        # mode: and
        mand = True if 'and' in pattern else False
        if mor:
            while pattern.count('or') > 0:
                pattern.remove('or')
        if mand:
            while pattern.count('and') > 0:
                pattern.remove('and')
        br = []
        for p in pattern:
            br.append(any([p in item[k] for k in keys]))
        if mor:
            return any(br)
        return all(br)

    def getPath(self, idx):
        ''' get current path from QModelIndex '''
        data = self.model.data_row(idx.row())
        cpath = QString(data[len(data)-1])
        return cpath

    def nextPath(self):
        row = self.model.nxt()
        self.tbl.selectRow(row)
        data = self.model.data_row(row)
        cpath = QString(data[len(data)-1])
        self.playNext.emit(cpath)
        return cpath

#    def clicked(self, idx):
#        raise NotImplementedError

    def double_clicked(self, idx):
        ''' double click on playlist emits playCurrent signal '''
        cpath = self.getPath(idx)
        self.playCurrent.emit(cpath)
        return cpath

#    def activated(self):
#        raise NotImplementedError

#    def entered(self):
#        raise NotImplementedError

#    def pressed(self, val1, val2):
#        raise NotImplementedError
    def append(self, item):
        self.tracks[item[-1]] = item
        self.model.append(item)

    def appendModel(self, item):
        self.model.append(item)
