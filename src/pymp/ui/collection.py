import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pymp import sqldb
from pymp.collection import Collection
from ..logger import init_logger
from ..model.tree import myModel

logger = init_logger()


class CollectionPanel(QWidget):
    '''
        Collection Tree
    '''
    def __init__(self, parent=None, playlist=None):
        QWidget.__init__(self, parent)
        self.playlist = playlist
        self._dclick_timer = QTimer(self)
        self.initUI()

    def initUI(self):
        ''' TODO: init user interface '''
        self.tre = QTreeView(self)
        self.model = myModel()
        self.tre.setModel(self.model)
        self.tre.setDragDropMode(QAbstractItemView.InternalMove)
        self.tre.dragEnabled()
        self.tre.acceptDrops()
        self.tre.showDropIndicator()
        self.tre.setExpandsOnDoubleClick(False)
        self.tre.setColumnWidth(0, 200)
        self.tre.setColumnWidth(1, 90)
        self.tre.setColumnWidth(2, 100)
        #self.tre.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.tre.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tre.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tre.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tre.customContextMenuRequested.connect(self.popup)
        self.tre.clicked.connect(self.clicked)
        #self.tre.activated.connect(self.activated)
        #self.tre.pressed.connect(self.pressed)
        self._dclick_timer.timeout.connect(self._dclick_timeout)
        vbox = QHBoxLayout(self)
        vbox.addWidget(self.tre, 1)
        self.setMinimumWidth(420)

    def usePattern(self, pattern):
        pattern = str(pattern).lower().strip()
        self.model.reset()
        self.model.setPattern(pattern)
        if pattern:
            self.tre.expandAll()

    def _dclick_timeout(self):
        '''
            called on timeout for double click timer
        '''
        logger.info('single click')
        index = self.idx
        self.tre.setExpanded(index, not self.tre.isExpanded(index))
        self._dclick_timer.stop()

    def clicked(self, index):
        '''
            start a double click timer for 300ms.
            if dclick: fill playlist with node-children
            if singleclick: open tree node
        '''
        self.idx = index
        if self._dclick_timer.isActive():
            self._dclick_timer.stop()
            node = self.model.nodeFromIndex(index)
            if isinstance(node.data, list):
                self.playlist.append(node.data)
            else:
                self._add_child_nodes(self.model.nodeFromIndex(index))
        else:
            self._dclick_timer.start(300)

    def _add_child_nodes(self, node):
        '''
            append list children to playlist recursively
        '''
        if node.hasChildren():
            for child in node.children:
                if isinstance(child.data, list):
                    self.playlist.append(child.data)
                if child.hasChildren():
                    self._add_child_nodes(child)

#    def activated(self):
#        raise NotImplementedError
#    def pressed(self):
#        raise NotImplementedError
    def popup(self, point):
        mindex = self.tre.indexAt(point)
        self.node = self.model.nodeFromIndex(mindex)
        data = self.node.data

        toolb = QToolBar(self.tre)
        popMenu = QMenu(self.tre)
        actionNew = toolb.addAction('Collection::ADD', self.addCollection)
        popMenu.addAction(actionNew)
        popMenu.exec_(self.tre.mapToGlobal(point))

    def addCollection(self):
        logger.info('add collection')
        path = unicode(QFileDialog.getExistingDirectory(
                        self,
                        'Choose dir',
                        '',
                        QFileDialog.ShowDirsOnly).toUtf8(), 'utf-8')
        if not path or path == '/':
            return False
        cpath, cname = os.path.split(path)
        col = {cname : path}
        sqldb.init_collections(col)
        c = Collection(cname,path)
        c.rescan()
