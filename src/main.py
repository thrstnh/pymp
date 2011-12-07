#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import os
from pymp.playlist import Playlist
import pymp.sqldb
from ui.slim import Ui_PympSlimView
from ui.table_model import *
from ui.tree_model import myModel
from pprint import pprint
from pymp.config import cfg


class PympSlimView(QtGui.QMainWindow, Ui_PympSlimView):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        self._initialized = False
        QtGui.QMainWindow.__init__(self, parent)

        self.uistyles = [str(style) for style in QtGui.QStyleFactory.keys()]
        self.uistyleid = 0
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(self.uistyles[self.uistyleid]))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())

        self.ui = Ui_PympSlimView()
        self.setupUi(self)
        self.player = None
        self._dclick = False
        self._dclick_timer = QTimer(self)
        self._timer_search = QTimer(self)
        self.connect_actions()
        self.init_playlist()
        self.init_treeview()
        self.init_tableview()
        self._show_tree_collection = True
        self._show_plain_lyric = False
        self.init_config()
        self.current_path = ''
#        self.init_phonon()
        self._initialized = True
        self.statusBar.showMessage('Statusbar')
        
    def init_playlist(self):
        self.playlist = Playlist('name', 'path', {})

    def init_config(self):
        self.tree_collection.setShown(self._show_tree_collection)
        self.plain_lyric.setShown(self._show_plain_lyric)

    def connect_actions(self):
        # toolbar
        self.toolb_new.clicked.connect(self.playlist_new)
        self.toolb_open.clicked.connect(self.playlist_open)
        self.toolb_save.clicked.connect(self.playlist_save)
        self.toolb_layout_left.clicked.connect(self.layout_left)
        self.toolb_layout_right.clicked.connect(self.layout_right)
        self.toolb_random.clicked.connect(self.random)
        self.toolb_repeat.clicked.connect(self.repeat)
        self.toolb_clear.clicked.connect(self.playlist_clear)
        self.toolb_focus.clicked.connect(self.track_focus)
        self.toolb_shuffle.clicked.connect(self.playlist_shuffle)
        self.toolb_settings.clicked.connect(self.settings)
        self.toolb_love_track.clicked.connect(self.lastfm_love)
        self.toolb_lastfm.clicked.connect(self.lastfm_login)

        # menubar
        self.actionAbout.triggered.connect(self.about)
        self.actionAdd_collection.triggered.connect(self.collection_add)
        self.actionNew_playlist.triggered.connect(self.playlist_new)
        self.actionOpen_playlist.triggered.connect(self.playlist_open)
        self.actionQuit.triggered.connect(self.quit)
        self.actionSave_playlist.triggered.connect(self.playlist_save)
        self.actionShow_collection.triggered.connect(self.show_collection)
        self.actionShow_lyric.triggered.connect(self.show_lyric)
        self.actionLook_and_feel.triggered.connect(self.lookandfeel)
        
        # ctrl bar
        self.toolb_prev.clicked.connect(self.prev)
        self.toolb_stop.clicked.connect(self.stop)
        self.toolb_play.clicked.connect(self.play)
        self.toolb_next.clicked.connect(self.next)
        self.toolb_mute.clicked.connect(self.mute)
        self.slider_volume.valueChanged.connect(self.scratch_volume)
        self.slider_time.valueChanged.connect(self.scratch_time)

        # search
        self.toolb_clear_search.clicked.connect(self.search_clear)
        self.line_search.returnPressed.connect(self.search_return)
        self.line_search.textChanged.connect(self.search_changed)
        self.line_search.editingFinished.connect(self.search_finished)

        # tree collection
        self.tree_collection.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_collection.customContextMenuRequested.connect(self.tree_popup)
        self.tree_collection.clicked.connect(self.tree_clicked)
        self.tree_collection.activated.connect(self.tree_activated)
        self.tree_collection.pressed.connect(self.tree_pressed)

        # table playlist
        self.table_playlist.clicked.connect(self.playlist_clicked)
        self.table_playlist.doubleClicked.connect(self.playlist_double_clicked)
        self.table_playlist.activated.connect(self.playlist_item_activated)
        self.table_playlist.entered.connect(self.playlist_item_entered)
        self.table_playlist.pressed.connect(self.playlist_item_pressed)

        self._dclick_timer.timeout.connect(self.dclick_timeout)
        self._timer_search.timeout.connect(self.search_table)

    def init_treeview(self):
        if self._initialized:
#            print "reinit treeview"
            self.tree_collection.reset()
        self._tree_model = myModel()
        self.tree_collection.setModel(self._tree_model)
        self.tree_collection.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.tree_collection.dragEnabled()
        self.tree_collection.acceptDrops()
        self.tree_collection.showDropIndicator()
        self.tree_collection.setExpandsOnDoubleClick(False)
        self.tree_collection.setColumnWidth(0, 200)
        self.tree_collection.setColumnWidth(1, 90)
        self.tree_collection.setColumnWidth(2, 100)

    def init_tableview(self):
        tm = MyTableModel(self)
        self.table_model = tm
        self.table_playlist.setModel(tm)

        self.table_playlist.setShowGrid(False)

        vh = self.table_playlist.verticalHeader()
        vh.setVisible(False)

        hh = self.table_playlist.horizontalHeader()
        hh.setStretchLastSection(True)

        self.table_playlist.setColumnHidden(0, True)
        self.table_playlist.setColumnHidden(tm.column_length()-1, True)
        return

    def playlist_new(self):
        print "playlist new"
        raise NotImplementedError
    def playlist_open(self):
        print "playlist open"
        raise NotImplementedError
    def playlist_save(self):
        print "playlist save"
        raise NotImplementedError
    def layout_left(self):
        self._show_tree_collection = not self._show_tree_collection
        self.tree_collection.setShown(self._show_tree_collection)

    def layout_right(self):
        self._show_plain_lyric = not self._show_plain_lyric
        self.plain_lyric.setShown(self._show_plain_lyric)

    def random(self):
        print "random"
        raise NotImplementedError
    def repeat(self):
        print "repeat"
        raise NotImplementedError
    def playlist_clear(self):
        print "playlist_clear"
        self.table_model.clear()
#        raise NotImplementedError
    def track_focus(self):
        print "track_focus"
        raise NotImplementedError
    def playlist_shuffle(self):
        print "playlist_shuffle"
        raise NotImplementedError
    def settings(self):
        print "settings"
        raise NotImplementedError
    def lastfm_login(self):
        print "lastfm_login"
        raise NotImplementedError
    def lastfm_love(self):
        print "lastfm_love"
        raise NotImplementedError
    def about(self):
        print "about"
        raise NotImplementedError
    def quit(self):
        print "good bye"
        sys.exit(0)
    def collection_add(self):
        print "collection_add"
        raise NotImplementedError
    def show_lyric(self):
        print "show_lyric"
        raise NotImplementedError
    def show_collection(self):
        print "show_collection"
        raise NotImplementedError
    def prev(self):
        print "prev"
        raise NotImplementedError

    def stop(self):
        self.player.stop()
        self._update_time_labels()

    def play(self):
        #TODO select current path
        self.init_phonon()
        self.player.setCurrentSource(Phonon.MediaSource(QString(self.current_path)))
        self.player.play()

    def init_phonon(self):
        if not self.player:
            self.player = Phonon.createPlayer(Phonon.MusicCategory)
            self.m_audio = Phonon.AudioOutput(Phonon.MusicCategory, self)
            Phonon.createPath(self.player, self.m_audio)
            self.player.setTickInterval(100)
            # actions
            self.player.tick.connect(self.player_tick)
            self.player.finished.connect(self.player_finished)
            # QSlider -> SeekSlider
            self.slider_time = Phonon.SeekSlider(self.player, self)

    def player_tick(self, time):
        self._update_time_labels()

    def _handle_time(self, time):
        m, s = divmod(time, 60)
        if m < 60:
            return "%02i:%02i" % (m, s)
        else:
            h, m = divmod(m, 60)
            return "%i:%02i:%02i" % (h, m, s)

    def player_finished(self):
        self._update_time_labels()
        self.next()

    def next(self):
        row = self.table_model.next()
        self.table_playlist.selectRow(row)
        data = self.table_model.data_row(row)
        self.current_path = '%s' % data[len(data)-1]
        self.play()

    def mute(self):
        self.m_audio.setMuted(not self.m_audio.isMuted())
        print "muted: ", self.m_audio.isMuted()

    def scratch_volume(self, val):
        val = float(val) / 100.
        print dir(self.m_audio)
        self.m_audio.setVolume(val)

    def _update_time_labels(self):
        cur_s = 0
        total_s = 0
        if self.player and self.player.state() == Phonon.PlayingState:
            cur_s = self.player.currentTime() / 1000.
            total_s = self.player.totalTime() / 1000.
        self.label_time_start.setText(self._handle_time(cur_s))
        self.label_time_stop.setText(self._handle_time(total_s))

    def scratch_time(self, time):
        if self.player and self.player.state() == Phonon.PlayingState:
            seek = (time * self.player.totalTime()) / 100
            self.player.seek(seek)
            self._update_time_labels()
        else:
            print "not playing... ", time

    def lookandfeel(self):
        if self.uistyleid >= len(self.uistyles)-1:
            self.uistyleid = 0
        else:
            self.uistyleid += 1
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(self.uistyles[self.uistyleid]))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())

    def search_clear(self):
        pass # already done in qtdesigner
    
    def search_return(self):
        if self._timer_search.isActive():
            self._timer_search.stop()
        self.search_table()
    
    def search_changed(self, val):
        if self._timer_search.isActive():
            self._timer_search.stop()
        self._timer_search.start(500)
        self._search_pattern = u"%s" % val

    def search_finished(self):
        if self._timer_search.isActive():
            self._timer_search.stop()

    def playlist_clicked(self, val1):
        print 'playlist_clicked: ', val1
        data = self.table_model.data_row(val1.row())
        self.current_path = '%s' % data[len(data)-1]
        print "current_path: ", type(self.current_path)

    def playlist_double_clicked(self, val1):
        print "playlist_double_clicked"
        raise NotImplementedError
        
    def playlist_pressed(self, val1, val2):
        print 'playlist_pressed: ', val1, val2
        
    def playlist_item_activated(self, item):
        print 'playlist_activated: ', item
        
    def playlist_item_changed(self, item):
        print 'playlist_changed: ', item
        
    def playlist_item_clicked(self, item):
        print 'playlist_item_clicked: ', item
        
    def playlist_item_double_clicked(self, item):
        print 'playlist_item_double_clicked: ', item
        
    def playlist_item_entered(self, item):
        print 'playlist_item_entered: ', item
        
    def playlist_item_pressed(self, item):
        print 'playlist_item_pressed: ', item

    def dclick_timeout(self):
        print "single click"
        index = self._tree_clicked_index
        self.tree_collection.setExpanded(index, not self.tree_collection.isExpanded(index))
        self._dclick_timer.stop()

    def search_table(self):
        if self._timer_search.isActive():
            self._timer_search.stop()
        print "table-filter: ", self._search_pattern

        
    def playlist_selection_changed(self):
        print 'playlist_selection_changed'
        
    def tree_activated(self, e):
        print "tree_activated"

    def tree_clicked(self, index):
        self._tree_clicked_index = index
        if self._dclick_timer.isActive():
            self._dclick_timer.stop()
            node = self._tree_model.nodeFromIndex(index)
            if isinstance(node.data, list):
                self.table_model.append(node.data)
            else:
                self._add_child_nodes(self._tree_model.nodeFromIndex(index))
        else:
            self._dclick_timer.start(300)

    def tree_popup(self, point):
        mindex = self.tree_collection.indexAt(point)
        node = self._tree_model.nodeFromIndex(mindex)
        self._tree_pop_node = node
        data = node.data

        toolb = QtGui.QToolBar(self.tree_collection)
        popMenu = QtGui.QMenu(self.tree_collection)

        if isinstance(data, list):
            print "MP3: ", data
            actionAdd = toolb.addAction('Track::ADD', self._pop_tree_track_add)
            actionDel = toolb.addAction('Track::DEL', self._pop_tree_track_del)
            popMenu.addAction(actionAdd)
            popMenu.addAction(actionDel)
        if data == 'COLLECTION':
            actionAdd = toolb.addAction('Collection::ADD', self._pop_tree_collection_add)
            actionRescan = toolb.addAction('Collection::RESCAN', self._pop_tree_collection_rescan)
            actionRescanStop = toolb.addAction('Collection::RESCAN_STOP', self._pop_tree_collection_rescan_stop)
            actionDel = toolb.addAction('Collection::DEL', self._pop_tree_collection_del)
            popMenu.addAction(actionAdd)
            popMenu.addSeparator()
            popMenu.addAction(actionRescan)
            if self._tree_model.collection_is_scanning(self._tree_pop_node.name):
                popMenu.addAction(actionRescanStop)
            popMenu.addSeparator()
            popMenu.addAction(actionDel)
        elif data == 'ARTIST':
            actionAdd = toolb.addAction('Artist::ADD', self._pop_tree_artist_add)
            actionDel = toolb.addAction('Artist::DEL', self._pop_tree_artist_del)
            popMenu.addAction(actionAdd)
            popMenu.addAction(actionDel)
        elif data == 'ALBUM':
            actionAdd = toolb.addAction('Album::ADD', self._pop_tree_album_add)
            actionDel = toolb.addAction('Album::DEL', self._pop_tree_album_del)
            popMenu.addAction(actionAdd)
            popMenu.addAction(actionDel)
        else:
            actionNew = toolb.addAction('Collection::ADD', self._pop_tree_collection_new)
            popMenu.addAction(actionNew)
        popMenu.exec_(self.tree_collection.mapToGlobal(point))

    def _pop_tree_collection_add(self):
        self._add_child_nodes(self._tree_pop_node)
        self.statusBar.showMessage("Playlist: %s files" % self.table_model.row_length())

    def _pop_tree_collection_new(self):
        path = unicode(QFileDialog.getExistingDirectory(
                        self,
                        'Choose dir',
                        cfg['PYMP_DIR'],
                        QFileDialog.ShowDirsOnly).toUtf8(), 'utf-8')       
        if not path or path == '/':
            return False
        cpath, cname = os.path.split(path)
        col = {cname : path}
        pymp.sqldb.init_collections(col)
        c = pymp.collection.Collection(cname,path)
        c.rescan()
        self.init_treeview()
        
    def _pop_tree_collection_rescan(self):
        name = self._tree_pop_node.name
        if not self._tree_model.collection_rescan(name):
            self.showMessage(u"collection is already scanning...")

    def showMessage(self, msg):
        ''' to del... '''
        self.show_msg(msg)

    def show_msg(self, msg):
        msgbox = QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()

    def _pop_tree_collection_rescan_stop(self):
        name = self._tree_pop_node.name
        if self._tree_model.collection_rescan_stop(name):
            self.showMessage(u"collection scan(%s) canceled" % name)
        else:
            self.showMessage(u"collection scannt immer noch??")

    def _pop_tree_collection_del(self):
        name = self._tree_pop_node.name
        ret = QMessageBox.question(self, u'Collection löschen?', u'Wirklich Collection %s löschen?' % name, QMessageBox.Yes,QMessageBox.No)
        if ret == QMessageBox.Yes:
            if self._tree_model.collection_delete(name):
                msg = QMessageBox()
                msg.setText(u"Collection deleted: %s" % name)
                msg.exec_()
                self.init_treeview()

    def _pop_tree_artist_add(self):
        print '_pop_tree_artist_add'
        self._add_child_nodes(self._tree_pop_node)
        self.statusBar.showMessage("Playlist: %s files" % self.table_model.row_length())
    def _pop_tree_artist_del(self):
        print '_pop_tree_artist_del'
    def _pop_tree_album_add(self):
        print '_pop_tree_album_add'
        self._add_child_nodes(self._tree_pop_node)
        self.statusBar.showMessage("Playlist: %s files" % self.table_model.row_length())
    def _pop_tree_album_del(self):
        print '_pop_tree_album_del'
    def _pop_tree_track_add(self):
        print '_pop_tree_track_add ', self._tree_pop_node
        node = self._tree_pop_node
        if isinstance(node.data, list):
            self.table_model.append(node.data)
        self.statusBar.showMessage("Playlist: %s files" % self.table_model.row_length())
    def _pop_tree_track_del(self):
        print '_pop_tree_track_del'

    def _add_child_nodes(self, node):
        if node.hasChildren():
            for child in node.children:
                if isinstance(child.data, list):
                    self.table_model.append(child.data)
                if child.hasChildren():
                    self._add_child_nodes(child)

    def tree_double_clicked(self, index):
        print "real dclick"
        
    def tree_pressed(self, e):
        pass
        #print "tree_mouse_press_event: ", e
        #raise NotImplementedError
    def tree_selection_changed(self, sel, dsel):
        pass
        #print "tree_selection_changed: ", sel, dsel
        #raise NotImplementedError


def main():
    app = QtGui.QApplication(sys.argv)
    window = PympSlimView()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
