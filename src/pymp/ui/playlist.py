import time
import random
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .tageditor import ID3Edit
from ..logger import init_logger
from ..model.table import MyTableModel, myQTableView
from ..config import init_env

logger = init_logger()
PYMPENV = init_env()


class PlaylistPanel(QWidget):
    '''
        Playlist Table

        click
        dclick

    '''
    # send signal on double click
    playCurrent = pyqtSignal(QString)
    playPrev = pyqtSignal(QString)
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
        self.tbl.setColumnHidden(self.model.columnCount(None)-1, True)
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
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.tbl, 1)
        #vbox = QVBoxLayout(self)
        self.tbl.clicked.connect(self.clicked)
        self.tbl.doubleClicked.connect(self.double_clicked)
        self.init_hdr()
        # TODO qt_layout decorator
#        self.tbl.activated.connect(self.activated)
#        self.tbl.entered.connect(self.entered)
#        self.tbl.pressed.connect(self.pressed)

    def init_hdr(self):
        self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.tbl.horizontalHeader().setStretchLastSection(True)
        self.tbl.horizontalHeader().resizeSection(0, 60)
        self.tbl.horizontalHeader().resizeSection(1, 180)
        self.tbl.horizontalHeader().resizeSection(2, 180)
        self.tbl.emit(SIGNAL("layoutChanged()"))

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

    def search(self, pattern=''):
        tstart = time.time()
        if not pattern:
            [self.appendModel(item) for (k, item) in self.tracks.items()]
        else:
            pattern = str(pattern.toUtf8()).lower().split()
            self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.model.clear()
            self.tbl.emit(SIGNAL("layoutChanged()"))
            for (k, v) in self.tracks.items():
                if self.__valid_entry(v, map(str.strip, pattern), (1, 2, 3)):
                    self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
                    self.appendModel(v)
                    self.tbl.emit(SIGNAL("layoutChanged()"))
        self.init_hdr()
        self.parent.statusBar().showMessage('%s Tracks' % (self.model.rowCount(None)))
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

    def _get_path(self, row):
        data = self.model.data_row(row)
        cpath = QString(data[len(data)-1])
        return cpath

    def _random(self):
        index = random.randint(0, self.model.length())
        if not PYMPENV['FAST_CLIENT']:
            return index
        seq = range(0, self.model.length())
        for _ in range(random.randint(0, 7)):
            random.shuffle(seq)
        val = seq[index]
        logger.info(':random key {}'.format(val))
        return val

    def _row_valid(self, row):
        if row >= self.model.length():
            return 0
        if row < 0:
            return self.model.length() - 1
        return row

    def _change_index(self, row, signal):
        row = self._row_valid(row)
        self._index_playing \
                = self._index_playing.sibling(row,
                        self._index_playing.column())
        self._index_selected = self._index_playing
        if PYMPENV['AUTO_FOCUS']:
            self.tbl.selectRow(row)
        cpath = self._get_path(row)
        signal.emit(cpath)
        return cpath

    def select_playing(self):
        self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.tbl.selectRow(self._index_playing.row())
        self.tbl.emit(SIGNAL("layoutChanged()"))

    def prev_path(self):
        if PYMPENV['RANDOM']:
            row = self._random()
        else:
            row = self._index_playing.row() - 1
        return self._change_index(row, self.playPrev)

    def next_path(self):
        if PYMPENV['RANDOM']:
            row = self._random()
        else:
            row = self._index_playing.row() + 1
        return self._change_index(row, self.playNext)

    def current_path(self):
        cpath = self._get_path(self._index_selected.row())
        self._index_playing = self._index_selected
        self.playCurrent.emit(cpath)
        return cpath

    def clicked(self, idx):
        logger.info('playlist clicked {}, {}'.format(idx.row(), idx.column()))
        self._index_selected = idx
        self.tbl.selectRow(idx.row())

    def double_clicked(self, idx):
        ''' double click on playlist emits playCurrent signal '''
        self._index_playing = idx
        cpath = self._get_path(idx.row())
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
