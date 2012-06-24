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
    # send signal on double click
    playCurrent = pyqtSignal(QString)
    playPrev = pyqtSignal(QString)
    playNext = pyqtSignal(QString)
    enqueue = pyqtSignal(list)
    dequeue = pyqtSignal(list)
    filled = pyqtSignal(float)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()
        # current tracks
        self.tracks = {}
        self._track_list = []
        self.parent = parent
        self._current_index = 0
        self._history = []
        self._history_level = -1
        self._queue = []

    def initUI(self):
        self.tbl = myQTableView(self)
        self.model = MyTableModel(self)
        self.tbl.setModel(self.model)
        self.tbl.set_model(self.model)
        self.tbl.setShowGrid(False)
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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#        self.tbl.customContextMenuRequested.connect(self.popup)
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
        # TODO qt_layout decorator
#        self.tbl.activated.connect(self.activated)
#        self.tbl.entered.connect(self.entered)
#        self.tbl.pressed.connect(self.pressed)

    def popup(self, point):
        if self._table_empty():
            return
        idx = self.tbl.selectionModel().currentIndex()
        data = self.model.data_row_(idx.row())

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
        self.model.clear_()

    def search(self, pattern=''):
        tstart = time.time()
        pattern = map(unicode.strip, unicode(pattern).split())
        mor = 'or' in pattern
        rows = (4, 5, 7, 23)
        pattern = filter(lambda p: len(p) >= PYMPENV['SEARCH_MIN_LENGTH'], pattern)
        if not pattern:
            self.model.set_data_(self._track_list)
        else:
            self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.model.clear_()
            for (k, v) in self.tracks.items():
                if self._match(v, pattern, rows, mode_or=mor):
                    self.appendModel(v)
            self.tbl.emit(SIGNAL("layoutChanged()"))
        self.parent.statusBar().showMessage('%s Tracks' % (self.model.rowCount(None)))
        tdiff = time.time() - tstart
        self.filled.emit(tdiff)
        logger.info(':fill {}s'.format(tdiff))

    def _match(self, item, pattern=[], keys=[], case_sensitive=False, mode_or=False):
        r'''example:
                item = ['Tenacious D', 'Tribute', 'Homemade', 'Rock']
                pattern = ['tenac', 'rock']
                keys = (0, 3)
                # would match every pattern in item with given index
        '''
        if not case_sensitive:
            item = [s.lower() if isinstance(s, basestring) else s for s in item]
            pattern = map(unicode.lower, pattern)
        b = map(lambda p: any([p in item[k] for k in keys]), pattern)
        return any(b) if mode_or else all(b)

    def _get_path(self, row):
        data = self.model.data_row_(row)
        cpath = QString(data[len(data)-1])
        return cpath

    def _current_row(self):
        return self.model.data_row_(self._current_index)

    def _current_row_selected(self):
        return self.model.data_row_(self._index_selected.row())

    def _random(self):
        if self._table_empty():
            return
        rows = self.model.rowCount(None)
        index = random.randint(0, rows)
        if not PYMPENV['FAST_CLIENT']:
            return index
        seq = range(0, rows)
        for _ in range(random.randint(0, 7)):
            random.shuffle(seq)
        val = seq[index]
        logger.info(':random key {}'.format(val))
        return val

    def _row_valid(self, row):
        if row >= self.model.rowCount(None):
            return 0
        if row < 0:
            return self.model.rowCount(None) - 1
        return row

    def _change_index(self, row, signal, append_history=True):
        row = self._row_valid(row)
        self._index_playing \
                = self._index_playing.sibling(row,
                                        self._index_playing.column())
        if PYMPENV['AUTO_FOCUS']:
            self.tbl.selectRow(row)
            self.tbl.scrollTo(self._index_playing, QAbstractItemView.PositionAtCenter)
        if append_history:
            self._history.append(self._current_row())
        cpath = self._get_path(row)
        signal.emit(cpath)
        return cpath

    def select_playing(self):
        if self._table_empty():
            return
        self.tbl.setFocus(True)
        self.tbl.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.tbl.selectRow(self._index_playing.row())
        self.tbl.scrollTo(self._index_playing, QAbstractItemView.PositionAtCenter)
        self.tbl.emit(SIGNAL("layoutChanged()"))
        self.parent.setFocus(True)

    def prev_path(self):
        if self._table_empty():
            return
        elif len(self._history) == 0:
            logger.info(':history empty')
        elif self._history_level <= - len(self._history):
            logger.info(':history first')
        else:
            self._history_level -= 1
            last = self._history[self._history_level]
            row = self.model.row_id_(last)
            if row:
                self._current_index = row
                self._change_index(self._current_index, self.playPrev, False)

    def next_path(self):
        if self._table_empty():
            return
        self._history_level = -1
        qitem = None
        if not self.queue_empty():
            qitem = self._queue.pop(0)
            logger.debug(':queue {}'.format(qitem))
            row = self.model.row_id_(qitem)
            if row:
                self._current_index = row
                self._change_index(self._current_index, self.playNext, False)
                return
        if PYMPENV['RANDOM']:
            self._current_index = self._random()
        else:
            self._current_index += 1
            if self._current_index > self.model.rowCount(None):
                self._current_index = 0
        return self._change_index(self._current_index, self.playNext)

    def _table_empty(self):
        empty = self.model.rowCount(None) == 0
        if not empty:
            self._index_playing = self.tbl.currentIndex()
        return empty

    def current_path(self):
        if self._table_empty():
            return
        self._history_level = -1
        self._current_index = self._index_selected.row()
        cpath = self._get_path(self._current_index)
        self._index_playing = self._index_selected
        self.playCurrent.emit(cpath)
        return cpath

    def clicked(self, idx):
        self._index_selected = idx
        self.tbl.selectRow(idx.row())
        self.parent.setFocus(True)

    def double_clicked(self, idx):
        ''' double click on playlist emits playCurrent signal '''
        self._index_playing = idx
        self._history_level = -1
        self._current_index = self._index_selected.row()
        cpath = self._get_path(idx.row())
        self.playCurrent.emit(cpath)
        self.parent.setFocus(True)
        self._history.append(self._current_row())
        return cpath

#    def activated(self):
#        raise NotImplementedError

#    def entered(self):
#        raise NotImplementedError

#    def pressed(self, val1, val2):
#        raise NotImplementedError
    def append(self, item):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.tracks[item[-1]] = item
        self._track_list.append(item)
        self.tbl.append(item)
        self.emit(SIGNAL("layoutChanged()"))

    def appendModel(self, item):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.tbl.append(item)
        self.emit(SIGNAL("layoutChanged()"))

    def enqueue_track(self):
        cr = self._current_row_selected()
        logger.info(':enqueue {}'.format(cr))
        self._queue.append(cr)
        self.enqueue.emit(cr)

    def queue_empty(self):
        return len(self._queue) == 0
