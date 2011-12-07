#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cPickle import dumps
from cPickle import load
from cPickle import loads
from cStringIO import StringIO
from copy import deepcopy
from pymp.collection import Collections
import pymp.sqldb

__all__ = ["myModel"]

class PyMimeData(QMimeData):
    """ The PyMimeData wraps a Python instance as MIME data.
    """
    # The MIME type for instances.
    MIME_TYPE = QString('application/x-ets-qt4-instance')

    def __init__(self, data=None):
        """ Initialise the instance.
        """
        QMimeData.__init__(self)

        # Keep a local reference to be returned if possible.
        self._local_instance = data

        if data is not None:
            # We may not be able to pickle the data.
            try:
                pdata = dumps(data)
            except:
                return

            # This format (as opposed to using a single sequence) allows the
            # type to be extracted without unpickling the data itself.
            self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata)

    @classmethod
    def coerce(cls, md):
        """ Coerce a QMimeData instance to a PyMimeData instance if possible.
        """
        # See if the data is already of the right type. If it is then we know
        # we are in the same process.
        if isinstance(md, cls):
            return md

        # See if the data type is supported.
        if not md.hasFormat(cls.MIME_TYPE):
            return None
        nmd = cls()
        nmd.setData(cls.MIME_TYPE, md.data())
        return nmd

    def instance(self):
        """ Return the instance.
        """
        if self._local_instance is not None:
            return self._local_instance

        io = StringIO(str(self.data(self.MIME_TYPE)))

        try:
            # Skip the type.
            load(io)

            # Recreate the instance.
            return load(io)
        except:
            pass

        return None

    def instanceType(self):
        """ Return the type of the instance.
        """
        if self._local_instance is not None:
            return self._local_instance.__class__

        try:
            return loads(str(self.data(self.MIME_TYPE)))
        except:
            pass

        return None

class myNode(object):
    def __init__(self, name, state, description, data, parent=None):
        self.name = name
        self.state = state
        self.description = description
        self.data = data
        self.parent = parent
        self.children = []
        self.setParent(parent)
        
    def setParent(self, parent):
        if parent != None:
            self.parent = parent
            self.parent.appendChild(self)
        else:
            self.parent = None

    def hasChildren(self):
        return len(self.children)>0

    def appendChild(self, child):
        self.children.append(child)

    def childAtRow(self, row):
        return self.children[row]

    def rowOfChild(self, child):
        for i, item in enumerate(self.children):
            if item == child:
                return i
        return -1

    def removeChild(self, row):
        value = self.children[row]
        self.children.remove(value)
        return True
    
    def __len__(self):
        return len(self.children)

    def __str__(self):
        return 'Node: %s %s' % (self.name, self.data)


class myModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(myModel, self).__init__(parent)
        self.treeView = parent
        self.headers = ['Item', 'State', 'type']
        self._init_collection()

        self.columns = 3
        # Create items
        self._load()

    def _init_collection(self):
        self.collections = Collections()
    
    def collection_rescan(self, name):
        '''
            returns: True, if collection scan started
                    False, if collection is already scanning
        '''
        if name not in self.collections.names():
            print "collection-name does not exist."
            return False
        if not self.collections[name].is_scanning():
            self.collections[name].rescan()
            return True
        return False

    def collection_rescan_stop(self, name):
        if name not in self.collections.names():
            print "collection-name does not exist."
            return False
        if self.collections[name].scanning:
            self.collections[name].stop_scan()
            return True
        return False

    def collection_is_scanning(self, name):
        if name not in self.collections.names():
            print "collection-name does not exist."
            return False
        return self.collections[name].scanning

    def collection_delete(self, name):
        if name not in self.collections.names():
            print "collection-name does not exist."
            return False
        if not self.collections[name].scanning:
            pymp.sqldb.delete_collection(self.collections[name].cid)
            return True
        else:
            print "can't delete collection(%s) while it is scanning..." % name
        return False

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):
        defaultFlags = QAbstractItemModel.flags(self, index)
        if index.isValid():
            return Qt.ItemIsEditable | Qt.ItemIsDragEnabled | \
                Qt.ItemIsDropEnabled | defaultFlags
        else:
            return Qt.ItemIsDropEnabled | defaultFlags

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

    def mimeTypes(self):
        types = QStringList()
        types.append('application/x-ets-qt4-instance')
        return types

    def mimeData(self, index):
        node = self.nodeFromIndex(index[0])
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True

        dragNode = mimedata.instance()
        parentNode = self.nodeFromIndex(parentIndex)

        # make an copy of the node being moved
        newNode = deepcopy(dragNode)
        newNode.setParent(parentNode)
        self.insertRow(len(parentNode)-1, parentIndex)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), parentIndex, parentIndex)
        return True
    
    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)
    
    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()
        return True

    def index(self, row, column, parent):
        node = self.nodeFromIndex(parent)
        return self.createIndex(row, column, node.childAtRow(row))

    def data(self, index, role):
        if role == Qt.DecorationRole:
            return QVariant()
        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop | Qt.AlignLeft))
        if role != Qt.DisplayRole:
            return QVariant()
        node = self.nodeFromIndex(index)
        if index.column() == 0:
            return QVariant(node.name)
        elif index.column() == 1:
            return QVariant(node.state)
        elif index.column() == 2:
            return QVariant(node.description)
        else:
            return QVariant()

    def columnCount(self, parent):
        return self.columns
    
    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        return len(node)

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()
        node = self.nodeFromIndex(child)
        if node is None:
            return QModelIndex()

        parent = node.parent
        if parent is None:
            return QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)
        assert row != - 1
        return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.root

    def _load(self):
        '''
        self.root = myNode('root', 'on', 'this is root', 'ROOT', None)
        collection = myNode('Collection n', 'on', 'collection', 'COLLECTION', self.root)
        artist = myNode('Artist n', 'on', 'artist', 'ARTIST', collection)
        album = myNode('Album n', 'on', 'album', 'ALBUM', artist)
        track = myNode('Track n', 'on', 'track', 'track', album)
        '''
        self.root = myNode('root', 'on', 'this is root', 'ROOT', None)
        self.__tree = {}
        cols = self.collections.get_collections()
        for cid, v in cols.items():
            cname = v['name']
            self.__tree[cname] = {}
            ctcount = pymp.sqldb.count_collection_tracks(cid)
            collectionNode = myNode(cname, "%s files" % ctcount, 'collection', 'COLLECTION', self.root)
            
            self.__tree[cname + 'node'] = collectionNode

            cnodeTracks = myNode('noid3', 'on', 'no id3 tag', 'NOID3', collectionNode)
            self.__tree[cname + 'tracks'] = cnodeTracks

            treedata = pymp.sqldb.tree_dict(cid, '')
            if not treedata:
                return
            for val in treedata:
                artist = val['tpe1']

                if val['talb']:
                    if val['tdrc']:
                        album = '%s %s' % (val['tdrc'], val['talb'])
                    else:
                        album = val['talb']
                else:
                    album = ''

                if val['tit2']:
                    if val['trck']:
                        title = '%s %s' % (val['trck'], val['tit2'])
                    else:
                        title = '%s' % val['tit2']
                else:
                    title = ''
                path = [val['tid'], val['tit2'], val['tpe1'], val['talb'], val['tcon'],
                    val['tdrc'], val['tlen'], val['trck'], val['path']]

                if not val['hid3']:
                    h, t = os.path.split(val['path'])
                    trackNode = myNode(t, 'on', 'noid3', 'NOID3', self.__tree[cname + 'tracks'])
                else:
                    if artist not in self.__tree[cname]:
                        if not artist:
                            continue
                        self.__tree[cname][artist] = {}
#                        count_files = pymp.sqldb.count_artist_files(cid, artist)
                        artistNode = myNode(artist, 'on', 'artist', 'ARTIST', self.__tree[cname + 'node'])
                        self.__tree[cname]['node'] = artistNode

                    if album not in self.__tree[cname][artist]:
                        if not album:
                            trackNode = myNode(artist, 'on', 'artist', 'Album', self.__tree[cname]['node'])
                            continue
                        self.__tree[cname][artist][album] = {}
                        albumNode = myNode(album, 'on', 'album', 'ALBUM', self.__tree[cname]['node'])
                        self.__tree[cname][artist]['node'] = albumNode

                    if title not in self.__tree[cname][artist][album]:
                        if album:
                            myNode(title, 'on', 'title', path, self.__tree[cname][artist]['node'])
