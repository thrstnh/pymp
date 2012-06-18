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
        self.parent = parent
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
        self.setMinimumWidth(280)

    def usePattern(self, pattern=''):
        pattern = str(pattern).lower().strip()
        self.model.reset()
        self.model.setPattern(pattern)
        if pattern:
            self.tre.expandAll()
        self.parent.setFocus(True)

    def _dclick_timeout(self):
        '''
            called on timeout for double click timer
        '''
        logger.info('single click')
        index = self.idx
        self.tre.setExpanded(index, not self.tre.isExpanded(index))
        self._dclick_timer.stop()
        self.parent.setFocus(True)

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
            self.parent.update_statusbar()
        else:
            self._dclick_timer.start(300)
        self.parent.setFocus(True)

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
        self.current_collection_name = self.node.name
        logger.info('collection:popup: {}'.format(self.current_collection_name))

        toolb = QToolBar(self.tre)
        popMenu = QMenu(self.tre)
        popMenu.addAction(
                toolb.addAction('Collection::ADD',
                                self.addCollection))
        def _not_root():
            return self.current_collection_name != 'ROOT'

        if _not_root():
            if self.model.collection_is_scanning(self.current_collection_name):
                popMenu.addAction(
                        toolb.addAction('Collection::STOP RESCAN',
                                        self.rescanCollectionStop))
            else:
                popMenu.addAction(
                        toolb.addAction('Collection::RESCAN',
                                        self.rescanCollection))
        if _not_root():
            popMenu.addAction(
                    toolb.addAction('Collection::DELETE',
                                    self.deleteCollection))
        popMenu.addAction(
                    toolb.addAction('reload',
                                    self.initUI))
        popMenu.exec_(self.tre.mapToGlobal(point))

    def addCollection(self):
        logger.info('collection:add: {}'.format(self.current_collection_name))
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

    def rescanCollection(self):
        logger.info('collection:rescan: {}'.format(self.current_collection_name))
        self.model.collection_rescan(self.current_collection_name)

    def rescanCollectionStop(self):
        logger.info('collection:rescan:stop: {}'.format(self.current_collection_name))
        self.model.collection_rescan_stop(self.current_collection_name)

    def deleteCollection(self):
        logger.info('collection:delete: {}'.format(self.current_collection_name))
        self.model.collection_delete(self.current_collection_name)
