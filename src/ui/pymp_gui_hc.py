#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author: thrstnh
email:  thrstn.hllbrnd@googlemail.com
date:   07.12.2011 16:15
"""
import sys
import os
import time
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from PyQt4.phonon import Phonon
from tree_model import myModel
from table_model import MyTableModel, myQTableView
from pymp.mp3 import PMP3
from pymp.config import cfg as PYMPCFG, LYRICS_DIR
import lyricwiki

pref = '../data/iconsets/default/'

cssStyle = '''
'''

iconset = {
           "arr_down" : os.path.join(pref, 'arr_down.png'),
           "arr_left" : os.path.join(pref + 'arr_left.png'),
           "arr_right" : os.path.join(pref + 'arr_right.png'),
           "arr_up" : os.path.join(pref + 'arr_up.png'),
           "cancel" : os.path.join(pref + 'cancel.png'),
           "clear" : os.path.join(pref + 'clear.png'),
           "cut" : os.path.join(pref + 'cut.png'),
           "delete" : os.path.join(pref + 'delete.png'),
           "error" : os.path.join(pref + 'error.png'),
           "exit" : os.path.join(pref + 'exit.png'),
           "filter" : os.path.join(pref + 'filter.png'),
           "focus" : os.path.join(pref + 'focus.png'),
           "layout_lm" : os.path.join(pref + 'layout_lm.png'),
           "layout_lp" : os.path.join(pref + 'layout_lp.png'),
           "layout_rm" : os.path.join(pref + 'layout_rm.png'),
           "layout_rp" : os.path.join(pref + 'layout_rp.png'),
           "lfm_f" : os.path.join(pref + 'lfm_f.png'),
           "lfm_t" : os.path.join(pref + 'lfm_t.png'),
           "love_track" : os.path.join(pref + 'love_track.png'),
           "new" : os.path.join(pref + 'new.png'),
           "ok" : os.path.join(pref + 'ok.png'),
           "open" : os.path.join(pref + 'open.png'),
           "playback_ff" : os.path.join(pref + 'playback_ff.png'),
           "playback_next" : os.path.join(pref + 'playback_next.png'),
           "playback_pause" : os.path.join(pref + 'playback_pause.png'),
           "playback_play" : os.path.join(pref + 'playback_play.png'),
           "playback_prev" : os.path.join(pref + 'playback_prev.png'),
           "playback_rew" : os.path.join(pref + 'playback_rew.png'),
           "playback_stop" : os.path.join(pref + 'playback_stop.png'),
           "playback_mute" : os.path.join(pref + 'speaker.png'),
           "pymp" : os.path.join(pref + 'pymp.png'),
           "random_f" : os.path.join(pref + 'random_f.png'),
           "random_t" : os.path.join(pref + 'random_t.png'),
           "refresh" : os.path.join(pref + 'refresh.png'),
           "repeat_f" : os.path.join(pref + 'repeat_f.png'),
           "repeat_t" : os.path.join(pref + 'repeat_t.png'),
           "save" : os.path.join(pref + 'save.png'),
           "search" : os.path.join(pref + 'search.png'),
           "settings" : os.path.join(pref + 'settings.png'),
           "shuffle" : os.path.join(pref + 'shuffle.png'),
           "speaker" : os.path.join(pref + 'speaker.png'),
           "warning" : os.path.join(pref + 'warning.png'),
           "lookandfeel" : os.path.join(pref + 'warning.png'),
           }


class PympGUI(QtGui.QMainWindow):
    '''
        MainWindow of the python music player (pymp)
    '''
    def __init__(self):
        super(PympGUI, self).__init__()
        
        self.actions = {}
        
        self.uistyles = [str(style) for style in QtGui.QStyleFactory.keys()]
        self.uistyleid = 0
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(self.uistyles[self.uistyleid]))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        
        #cssStyle = "border: 1px solid black; padding: 1px;"
        #self.setStyleSheet(cssStyle)
        
        self.initUI()

    def initUI(self):
        ''' TODO: init user interface'''

        
        # actions in a dict :)
        self.actionsDict = {
                         'addCollection' :  ['Add &Collection', 'Ctrl+Q', 'Add Collection', QtGui.qApp.quit, iconset['new']],
                         'newPlaylist' :    ['New &Playlist', 'Ctrl+P', 'New Playlist', QtGui.qApp.quit, iconset['new']],
                         'openPlaylist' :   ['Open Playlist', 'Ctrl+P', 'Open Playlist', QtGui.qApp.quit, iconset['open']],
                         'savePlaylist' :   ['Save Playlist', 'Ctrl+P', 'Save Playlist', QtGui.qApp.quit, iconset['save']],
                         'viewCollection' : ['View Collection', 'Ctrl+I', 'View Collection Panel', QtGui.qApp.quit, iconset['cancel']],
                         'viewLyric' :      ['View Lyric', 'Ctrl+L', 'View Lyric Panel', QtGui.qApp.quit, iconset['cancel']],
                         # ctrl actions
                         'playback_ff' :    ['FF', 'Ctrl+Q', 'Forward', QtGui.qApp.quit, iconset['playback_ff']],
                         'playback_next' :  ['Next', 'Ctrl+Q', 'Next Track', QtGui.qApp.quit, iconset['playback_next']],
                         'playback_pause' : ['Pause', 'Ctrl+Q', 'Pause', QtGui.qApp.quit, iconset['playback_pause']],
                         'playback_play' :  ['Play', 'Ctrl+Q', 'Play', QtGui.qApp.quit, iconset['playback_play']],
                         'playback_prev' :  ['Prev', 'Ctrl+Q', 'Prev', QtGui.qApp.quit, iconset['playback_prev']],
                         'playback_rew' :   ['Rew', 'Ctrl+Q', 'Rew', QtGui.qApp.quit, iconset['playback_rew']],
                         'playback_stop' :  ['Stop', 'Ctrl+Q', 'Stop', QtGui.qApp.quit, iconset['playback_stop']],
                         'playback_mute' :  ['Mute', 'Ctrl+Q', 'Mute', QtGui.qApp.quit, iconset['playback_mute']],
                         'lookandfeel' :    ['look and feel', 'Ctrl+F', 'Change look and feel', self.lookandfeel, iconset['lookandfeel']],
                         'shuffle' :        ['shuffle', 'Ctrl+F', 'shuffle true/false', self.defAction, iconset['random_f']],
                         'repeat' :         ['repeat', 'Ctrl+F', 'repeat true/false', self.defAction, iconset['repeat_f']],
                         'clear' :          ['clear Playlist', 'Ctrl+F', 'clear playlist', self.defAction, iconset['clear']],
                         'help' :           ['help', 'Ctrl+F', 'help', QtGui.qApp.quit, iconset['cancel']],
                         'about' :          ['About pymp', 'Ctrl+F', 'about', QtGui.qApp.quit, iconset['cancel']],
                         'exit' :           ['Exit', 'Ctrl+Q', 'Exit Application', QtGui.qApp.quit, iconset['exit']],
                         }
        
        # compute actions-dict
        for (k,v) in self.actionsDict.items():
            (_name, _shortcut, _statustip, _action, _icon) = v
            self.actions[k] = self.qtregister_action(_name, _shortcut, _statustip, _action, _icon)
        
        menubar = self.menuBar()    
        fileMenu = menubar.addMenu('&File')
        viewMenu = menubar.addMenu('&View')
        playbackMenu = menubar.addMenu('&Playback')
        helpMenu = menubar.addMenu('&Help')
        [fileMenu.addAction(self.actions[k]) for k in ['addCollection', 'newPlaylist', 'openPlaylist', 'savePlaylist', 'exit']]
        [viewMenu.addAction(self.actions[k]) for k in ['help', 'viewLyric', 'lookandfeel']]
        [playbackMenu.addAction(self.actions[k]) for k in ['shuffle']]
        [helpMenu.addAction(self.actions[k]) for k in ['viewCollection', 'about']]

        self.statusBar()
        self.statusBar().showMessage('Ready')
        
        self.toolbar = self.addToolBar('Exit')
        [self.toolbar.addAction(self.actions[_]) for _ in self.actionsDict.keys()]
        
        self.setGeometry(20, 20, 1220, 620)
        self.setWindowTitle('pymp')
        
        mainpanel = QtGui.QWidget(self)
        
        left = QtGui.QFrame(self)
        left.setFrameShape(QtGui.QFrame.StyledPanel)
        center = QtGui.QFrame(self)
        center.setFrameShape(QtGui.QFrame.StyledPanel)
        right = QtGui.QFrame(self)
        right.setFrameShape(QtGui.QFrame.StyledPanel)
        
        splitterMain = QtGui.QSplitter(QtCore.Qt.Horizontal)
        
        # controls
        self.controlBar = ControlBar(self)
        self.searchBarCollection = SearchBar(self)
        self.searchBarPlaylist = SearchBar(self)
        self.plsPanel = PlaylistPanel(self)
        self.colPanel = CollectionPanel(self, self.plsPanel)
        self.trackInfo = TrackInfoBar(self)
        self.lyricPanel = LyricPanel(self)
        
        hbox = QtGui.QHBoxLayout(self)
        
        hbox.setSpacing(0)
        vboxCollection = QtGui.QVBoxLayout(self)
        vboxCollection.addWidget(self.searchBarCollection)
        vboxCollection.addWidget(self.colPanel, 1)
        left.setLayout(vboxCollection)
        
        vboxPlaylist = QtGui.QVBoxLayout(self)
        vboxPlaylist.addWidget(self.searchBarPlaylist)
        vboxPlaylist.addWidget(self.plsPanel, 1)
        vboxPlaylist.addWidget(self.trackInfo)
        vboxPlaylist.addWidget(self.controlBar)
        center.setLayout(vboxPlaylist)
        
        vboxLyric = QtGui.QVBoxLayout(self)
        vboxLyric.addWidget(self.lyricPanel, 1)
        right.setLayout(vboxLyric)
        
        splitterMain.addWidget(left)
        splitterMain.addWidget(center)
        splitterMain.addWidget(right)
        
        hbox.addWidget(splitterMain)
        
        self.setCentralWidget(splitterMain)
        self.show()
    
    def defAction(self):
        print "TODO: default action"
        raise NotImplementedError
    
    def qtregister_action(self, name, shortcut, statustip, triggeraction, image):
        ''' TODO: register a qt-action the lazy way'''
        action = QtGui.QAction(QtGui.QIcon(image), name, self)
        action.setShortcut(shortcut)
        action.setStatusTip(statustip)
        action.triggered.connect(triggeraction)
        return action
    
    def lookandfeel(self):
        if self.uistyleid >= len(self.uistyles)-1:
            self.uistyleid = 0
        else:
            self.uistyleid += 1
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(self.uistyles[self.uistyleid]))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
    
    def showEvent(self, arg1):
        ''' show user interface '''
        # NOW init player, after gui shows up
        self.player = PlayerPhonon(self)
        # connect some actions
        self.controlBar.onPrev.connect(self.player.prev)
        self.controlBar.onStop.connect(self.player.stop)
        self.controlBar.onPlay.connect(self.player.play)
        self.controlBar.onNext.connect(self.player.next)
        self.controlBar.onMute.connect(self.player.mute)
        self.controlBar.onVolume.connect(self.player.volume)
        self.controlBar.onTime.connect(self.player.time)
        self.plsPanel.playCurrent.connect(self.player.play)
        self.plsPanel.playCurrent.connect(self.trackInfo.track)
        self.plsPanel.playNext.connect(self.player.play)
        self.plsPanel.playNext.connect(self.trackInfo.track)
        self.player.timeStart.connect(self.controlBar.setTimeStart)
        self.player.timeTotal.connect(self.controlBar.setTimeTotal)
        self.player.timeScratched.connect(self.controlBar.timeChangeValue)
        self.trackInfo.fetchLyrics.connect(self.lyricPanel.search)
        self.searchBarPlaylist.timerExpired.connect(self.plsPanel.usePattern)
        self.searchBarPlaylist.clearSearch.connect(self.plsPanel.usePattern)
        self.searchBarCollection.timerExpired.connect(self.colPanel.usePattern)
        self.searchBarCollection.clearSearch.connect(self.colPanel.usePattern)
        #self.searchBarPlaylist.search.connect(self.plsPanel.usePattern)
        

class PlaylistPanel(QtGui.QWidget):
    '''
        Playlist Table
        
        click
        dclick
        
    '''
    # send signal on double click
    playCurrent = QtCore.pyqtSignal(QtCore.QString)
    playNext = QtCore.pyqtSignal(QtCore.QString)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
        # current tracks
        self.tracks = {}
    
    def initUI(self):
        ''' TODO: init user interface '''
        self.tbl = myQTableView(self) #QtGui.QTableView(self)
        self.model = MyTableModel()
        self.tbl.setModel(self.model)
        self.tbl.setShowGrid(False)
        self.tbl.setColumnHidden(0, True)
        self.tbl.setColumnHidden(self.model.column_length()-1, True)
        self.tbl.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tbl.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tbl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tbl.setSortingEnabled(True)
        self.tbl.setWordWrap(False)
        self.tbl.setAlternatingRowColors(True)
        self.tbl.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tbl.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tbl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #self.tbl.setRowHeight()
        self.tbl.resizeRowsToContents()
        vh = self.tbl.verticalHeader()
        vh.setVisible(False)
        vh.setDefaultSectionSize(14)
        hh = self.tbl.horizontalHeader()
        hh.setStretchLastSection(True)
        
        self.toolbar = QtGui.QToolBar('Clear Playlist')
        ac = QtGui.QAction(QtGui.QIcon(iconset['clear']), "Clear Playlist", self)
        ac.setStatusTip("Clear Playlist")
        ac.triggered.connect(self.clearPlaylist)
        self.toolbar.addAction(ac)
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(self.tbl, 1)
        hbox.addWidget(self.toolbar)
        
        #vbox = QtGui.QVBoxLayout(self)
        
#        self.tbl.clicked.connect(self.clicked)
        self.tbl.doubleClicked.connect(self.double_clicked)
#        self.tbl.activated.connect(self.activated)
#        self.tbl.entered.connect(self.entered)
#        self.tbl.pressed.connect(self.pressed)

    def clearPlaylist(self):
        self.model.clear()
    
    def usePattern(self, pattern):
        print "rows: ", self.model.row_length()
        print "cols: ", self.model.column_length()
        
        
        if not pattern:
            [self.appendModel(item) for (k, item) in self.tracks.items()] 
        else:
            pattern = str(pattern).lower().split()
            match = False
            self.tbl.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
            self.model.clear()
            self.tbl.emit(QtCore.SIGNAL("layoutChanged()"))
            for (k, v) in self.tracks.items():
                if self.__valid_entry(v, map(str.strip, pattern)):
                    self.appendModel(v)
                    self.tbl.emit(QtCore.SIGNAL("layoutChanged()"))
                    continue
                
        print "usePattern finished"
        print "rows: ", self.model.row_length()
        print "cols: ", self.model.column_length()
        self.tbl.emit(QtCore.SIGNAL("layoutChanged()"))
    
    def __valid_entry(self, item, pattern=[]):
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
            p = p.strip()
            b0 = b1 = b2 = b3 = False
            #if item[-1]: # path
            #    if p in item[-1].lower():
            #        b0 = True
            if item[1]: # title
                if p in item[1].lower():
                    b1 = True
            if item[2]: # artist
                if p in item[2].lower():
                    b2 = True
            if item[3]: # album
                if p in item[3].lower():
                    b3 = True
            br.append(any([b0, b1, b2, b3]))

        if len(pattern) == 2 or mor:
            return any(br)
        return all(br)

    def getPath(self, idx):
        ''' get current path from QModelIndex '''
        data = self.model.data_row(idx.row())
        cpath = QtCore.QString(data[len(data)-1])
        return cpath
    
    def nextPath(self):
        row = self.model.next()
        self.tbl.selectRow(row)
        data = self.model.data_row(row)
        cpath = QtCore.QString(data[len(data)-1])
        self.playNext.emit(cpath)
        return cpath
    
#    def clicked(self, idx):
#        print "playlist::clicked"
#        raise NotImplementedError
        
    def double_clicked(self, idx):
        ''' double click on playlist emits playCurrent signal '''
        cpath = self.getPath(idx)
        self.playCurrent.emit(cpath)
        return cpath
            
#    def activated(self):
#        print "playlist::activated"
#        raise NotImplementedError

#    def entered(self):
#        print "playlist::entered"
#        raise NotImplementedError
    
#    def pressed(self, val1, val2):
#        print "playlist::pressed ", val1, val2
#        raise NotImplementedError
    def append(self, item):
        self.tracks[item[-1]] = item
        self.model.append(item)
    
    def appendModel(self, item):
        self.model.append(item)
        


class CollectionPanel(QtGui.QWidget):
    '''
        Collection Tree
    '''
    def __init__(self, parent=None, playlist=None):
        QtGui.QWidget.__init__(self, parent)
        self.playlist = playlist
        self._dclick_timer = QtCore.QTimer(self)
        self.initUI()
    
    def initUI(self):
        ''' TODO: init user interface '''
        self.tre = QtGui.QTreeView(self)
        self.model = myModel()
        self.tre.setModel(self.model)
        self.tre.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.tre.dragEnabled()
        self.tre.acceptDrops()
        self.tre.showDropIndicator()
        self.tre.setExpandsOnDoubleClick(False)
        self.tre.setColumnWidth(0, 200)
        self.tre.setColumnWidth(1, 90)
        self.tre.setColumnWidth(2, 100)
        #self.tre.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.tre.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tre.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tre.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tre.customContextMenuRequested.connect(self.popup)
        self.tre.clicked.connect(self.clicked)
        #self.tre.activated.connect(self.activated)
        #self.tre.pressed.connect(self.pressed)
        
        self._dclick_timer.timeout.connect(self._dclick_timeout)
     
        vbox = QtGui.QHBoxLayout(self)
        vbox.addWidget(self.tre, 1)
        
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
        print "single click"
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
#        print "activated"
#        raise NotImplementedError
#    def pressed(self):
#        print "pressed"
#        raise NotImplementedError
    def popup(self, point):
        mindex = self.tre.indexAt(point)
        self.node = self.model.nodeFromIndex(mindex)
        data = self.node.data

        toolb = QtGui.QToolBar(self.tre)
        popMenu = QtGui.QMenu(self.tre)
        actionNew = toolb.addAction('Collection::ADD', self.addCollection)
        popMenu.addAction(actionNew)
        popMenu.exec_(self.tre.mapToGlobal(point))
    
    def addCollection(self):
        print "add collection"


class LyricPanel(QtGui.QWidget):
    '''
        load lyric from lyricwiki in background
    '''    
    def __init__(self, parent=None):
        ''' TODO: init user interface '''
        QtGui.QWidget.__init__(self, parent)
        self.artist = ''
        self.track = ''
        self.monkey = None
        self.initUI()
    
    def initUI(self):
        ''' init user interface '''
        self.lblTrackInfo = QtGui.QLabel('')
        self.txt = QtGui.QTextEdit(self)
        self.txt.setReadOnly(True)
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.lblTrackInfo)
        vbox.addWidget(self.txt, 1)
         
    def search(self, artist, track):
        ''' search a lyrics with a thread '''
        # clear
        self.lblTrackInfo.setText('')
        self.txt.setText('')
        # set
        self.artist = '%s' % artist
        self.track = '%s' % track
        # search
        self.monkey = LyricWorker(self, self.artist, self.track)
        self.monkey.start()
        self.monkey.lyricFetched.connect(self.lyricChanged)
    
    def lyricChanged(self, lyr):
        ''' change label and textedit '''
        self.lblTrackInfo.setText('%s - %s' % (self.artist, self.track))
        self.txt.setText(lyr)
        
    def showEvent(self, arg1):
        ''' show user interface '''
        if self.monkey:
            self.monkey.start()        


class LyricWorker(QtCore.QThread):
    '''
        Fetch Lyrics from LyricsWiki
    '''
    # signal called after lyrics fetched
    lyricFetched = QtCore.pyqtSignal(QtCore.QString)
    
    def __init__(self, parent, artist, title):
        QtCore.QThread.__init__(self)
        self.artist = artist
        self.title = title
    
    def run(self):
        lyr = None
        if self.artist and self.title:
            lyr = self._read()
            if not lyr:
                lyr = lyricwiki.get_lyrics(self.artist, self.title)
                if lyr:
                    lyr = "%s - %s\n\n%s" % (self.artist, self.title, lyr)
                    self._save(lyr)
        else:
            print "worker got only: %s - %s" % (self.artist, self.title)
        if lyr:
            self.lyricFetched.emit(lyr)
            return
        else:
            print "QThread filed?..."
            self.lyricFetched.emit('no lyrics found...')
        return
    
    def _read(self):
        '''
            read lyrics from lyric-dir
        '''
        fp = os.path.join(PYMPCFG[LYRICS_DIR], "%s-%s.txt" % (self.artist, self.title))
        try:
            with open(fp, 'r') as f:
                lyr = f.read()
            return lyr
        except Exception, e:
            print("Lyrics Datei nicht gefunden: %s" % (fp))
        return ''

    def _save(self, lyr):
        '''
            save lyrics to lyric-dir for offline lyrics
        '''
        fp = os.path.join(PYMPCFG[LYRICS_DIR], "%s-%s.txt" % (self.artist, self.title))
        with open(fp, 'w') as f:
            f.write(lyr.encode('utf-8'))


class TrackInfoBar(QtGui.QWidget):
    '''
        Track Information Panel with current track
    '''
    # fetch lyrics with new track information to keep the right chain
    fetchLyrics = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
        self.artist = ''
        self.title = ''
        self.album = ''
        self.year = ''
        self.tracknr = ''
        self.genre = ''
    
    def initUI(self):
        ''' TODO: init user interface '''
        self.customLabel = QtGui.QLabel(self)

        vbox = QtGui.QVBoxLayout(self)
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(self.customLabel)
        vbox.addLayout(hbox)
    
    def track(self, qstr):
        '''
            fill fields with data
        '''
        mpfile = PMP3(qstr)
        self.artist = mpfile.artist
        self.title = mpfile.title
        self.album = mpfile.album
        self.year = mpfile.year
        self.tracknr = mpfile.trackno
        self.genre = mpfile.genre
        
        self.updateInformation()
        self.fetchLyrics.emit(self.artist, self.title)
    
    def updateInformation(self):
        '''
            sync vars with gui-labels
        '''
        tx = '%s\t-\t%s \n%s\t (%s, %s) \t %s' % (self.artist, self.title, self.album, self.year, self.tracknr, self.genre)
        self.customLabel.setText(tx)


class SearchBar(QtGui.QWidget):
    '''
        Control Panel for search patterns
    '''
    search = QtCore.pyqtSignal(QtCore.QString)
    clearSearch = QtCore.pyqtSignal(QtCore.QString)
    timerExpired = QtCore.pyqtSignal(QtCore.QString)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._search_timer = QtCore.QTimer(self)
        self.initUI()
        
    def initUI(self):
        ''' TODO: init user interface '''
        #pref = '../data/'
        #cssButton = "border-style: flat; border-width: 0px; border-color: black;"
        clr = QtGui.QPushButton(QtGui.QIcon(iconset['cancel']), "", self)
        clr.setFocusPolicy(QtCore.Qt.NoFocus)
        clr.clicked.connect(self.clrSearch)
        clr.setMinimumSize(QtCore.QSize(16,16))
        clr.setMaximumSize(QtCore.QSize(16,16))
        #clr.setStyleSheet(cssButton)
        
        self._search_timer.timeout.connect(self.searchTimeout)
        
        self.line = QtGui.QLineEdit('', self)
        self.line.textChanged.connect(self.txChanged)
        self.line.returnPressed.connect(self.txReturn)
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(clr)
        hbox.addWidget(self.line, 1)
    
    def txChanged(self, t):
        self.pattern = self.line.text()
        self.search.emit(self.pattern)
        
        '''
            start a double click timer for 300ms.
            if dclick: fill playlist with node-children
            if singleclick: open tree node
        '''
        if self._search_timer.isActive():
            self._search_timer.stop()
        self._search_timer.start(1000)
    
    def txReturn(self):
        self.search.emit(self.pattern)
        #self.pattern = self.line.text()
        #self.search.emit(self.pattern)
    
    def clrSearch(self):
        ''' clear search '''
        self.pattern = ''
        self.line.setText(self.pattern)
        self.clearSearch.emit(self.pattern)
    
    def searchTimeout(self):
        self._search_timer.stop()
        self.timerExpired.emit(self.pattern)


class ControlBar(QtGui.QWidget):
    '''
        Control Panel for prev, play, stop, next, mute and volume
    '''
    # some new slots
    onPrev = QtCore.pyqtSignal()
    onStop = QtCore.pyqtSignal()
    onPlay = QtCore.pyqtSignal()
    onNext = QtCore.pyqtSignal()
    onMute = QtCore.pyqtSignal()
    onPlay = QtCore.pyqtSignal()
    onVolume = QtCore.pyqtSignal(int)
    onTime = QtCore.pyqtSignal(int)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
    
    def initUI(self):
        ''' TODO: init user interface'''
        pref = '../data/'
        cssButton = "border-style: flat; border-width: 0px; border-color: black;"
        cssDEBUG = "background-color: black; border-style: flat; border-width: 0px; border-color: black;"
        
        #cssButton = cssDEBUG
        
        #self.setStyleSheet(cssDEBUG)
        
        sze = QtCore.QSize(16, 16)
        
        prev = QtGui.QPushButton(QtGui.QIcon(iconset['playback_rew']), "", self)
        prev.setFocusPolicy(QtCore.Qt.NoFocus)
        prev.clicked.connect(self.onPrev.emit)
        prev.setMinimumSize(sze)
        prev.setMaximumSize(sze)
        #prev.setStyleSheet(cssButton)
        
        stop = QtGui.QPushButton(QtGui.QIcon(iconset['playback_stop']), "", self)
        stop.setFocusPolicy(QtCore.Qt.NoFocus)
        stop.clicked.connect(self.onStop.emit)
        stop.setMinimumSize(sze)
        stop.setMaximumSize(sze)
        #stop.setStyleSheet(cssButton)
        
        play = QtGui.QPushButton(QtGui.QIcon(iconset['playback_play']), "", self)
        play.setFocusPolicy(QtCore.Qt.NoFocus)
        play.clicked.connect(self.onPlay.emit)
        play.setMinimumSize(sze)
        play.setMaximumSize(sze)
        #play.setStyleSheet(cssButton)
        
        nxt = QtGui.QPushButton(QtGui.QIcon(iconset['playback_next']), "", self)
        nxt.setFocusPolicy(QtCore.Qt.NoFocus)
        nxt.clicked.connect(self.onNext.emit)
        nxt.setMinimumSize(sze)
        nxt.setMaximumSize(sze)
        #nxt.setStyleSheet(cssButton)
        
        mute = QtGui.QPushButton(QtGui.QIcon(iconset['playback_mute']), "", self)
        mute.setFocusPolicy(QtCore.Qt.NoFocus)
        mute.clicked.connect(self.onMute.emit)
        mute.setMinimumSize(sze)
        mute.setMaximumSize(sze)
        #mute.setStyleSheet(cssButton)
        
        sldVol = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sldVol.setFocusPolicy(QtCore.Qt.NoFocus)
        sldVol.valueChanged[int].connect(self.volChangeValue)
        sldVol.valueChanged[int].connect(self.onVolume.emit)
        
        self.tstart = QtGui.QLabel("00:00", self)
        
        sldTime = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sldTime.setFocusPolicy(QtCore.Qt.NoFocus)
        sldTime.valueChanged[int].connect(self.timeChangeValue)
        sldTime.valueChanged[int].connect(self.onTime.emit)
        
        self.ttotal = QtGui.QLabel("23:59", self)
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(prev, 0)
        hbox.addWidget(stop, 0)
        hbox.addWidget(play)
        hbox.addWidget(nxt)
        hbox.addWidget(mute)
        hbox.addWidget(sldVol)
        hbox.addWidget(self.tstart)
        hbox.addWidget(sldTime, 1)
        hbox.addWidget(self.ttotal)
    
    def setTimeStart(self, time):
        self.tstart.setText(time)
    
    def setTimeTotal(self, time):
        self.ttotal.setText(time)
        
    def volChangeValue(self, value):
        ''' TODO: slider changed value'''
        print 'volume ',
        if value == 0:
            print "muted"
        elif value == 99:
            print "max"
        else:
            print value
    
    def timeChangeValue(self, value):
        ''' TODO: slider changed value'''
        print 'time ',
        if value == 0:
            print "muted"
        elif value == 99:
            print "max"
        else:
            print value
        
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        #rect = QRect(0, 0, self.width(), self.height())
        #qp.drawText(rect, Qt.AlignCenter, "self.text()")
        qp.end()


class ID3Edit(QtGui.QDialog):
    '''
        ID3 Tag Editor
    '''
    def __init__(self, parent=None, fp=None):
        QtGui.QDialog.__init__(self, parent)
        self.fp = fp
        self.data = self.load(self.fp)        
        self.initUI()
        
    def initUI(self):
        print self.data
        vbox = QtGui.QVBoxLayout(self)
        for (k,v) in self.data.items():
            hbox = QtGui.QHBoxLayout(self)
            lbl = QtGui.QLabel(str(k), self)
            line = QtGui.QLineEdit(str(v), self)
            hbox.addWidget(lbl)
            hbox.addWidget(line, 1)
            vbox.addLayout(hbox)
            
        hbox = QtGui.QHBoxLayout(self)
        ok = QtGui.QPushButton(QtGui.QIcon('../data/iconsets/default/ok.png'), "", self)
        ok.clicked.connect(self.onOk)
        cancel = QtGui.QPushButton(QtGui.QIcon('../data/cancel.png'), "", self)
        cancel.clicked.connect(self.onCancel)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        vbox.addLayout(hbox)
        
        #self.setLayout(vbox)
        self.setWindowTitle('ID3 Editor')
        self.resize(300, 800)
    
    def load(self, fp):
        '''
            load mp3 id3 meta data from file as dict
        '''
        return PMP3(fp).all()
    
    def onOk(self):
        ''' exit dialog with ok'''
        print "ok"
        self.close()
    
    def onCancel(self):
        ''' exit dialog with cancel '''
        print "cancel"
        self.close()

class PlayerPhonon(QtCore.QObject):
    '''
        Handle for the Phonon class
    '''
    # tick for player
    timeStart = QtCore.pyqtSignal(QtCore.QString)
    timeTotal = QtCore.pyqtSignal(QtCore.QString)
    timeScratched = QtCore.pyqtSignal(int)
    volScratched = QtCore.pyqtSignal(int)
    
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        self.player = Phonon.createPlayer(Phonon.MusicCategory)
        self.m_audio = Phonon.AudioOutput(Phonon.MusicCategory, parent)
        Phonon.createPath(self.player, self.m_audio)
        self.player.setTickInterval(100)
        # actions
        self.player.tick.connect(self.tick)
        self.player.finished.connect(self.finished)
        
        #print Phonon.BackendCapabilities.availableAudioEffects()
        # QSlider -> SeekSlider
        #self.slider_time = Phonon.SeekSlider(self.player, self)
        
    def play(self, cpath):
        self.player.setCurrentSource(Phonon.MediaSource(cpath))
        self.player.play()
        
    def stop(self):
        self.player.stop()
        
    def next(self):
        print "Player::next"
        
    def prev(self):
        print "Player::prev"
        
    def mute(self):
        self.m_audio.setMuted(not self.m_audio.isMuted())
        print "muted: ", self.m_audio.isMuted()
        
    def random(self):
        print "Player::random"
        
    def repeat(self):
        print "Player::repeat"
        
    def volume(self, val):
        ''' TODO: slider changed value'''
        val = float(val) / 100.
        #print dir(self.m_audio)
        self.m_audio.setVolume(val)
        self.volScratched.emit(val)
            
    def time(self, val):
        ''' TODO: slider changed value'''
        if self.player and self.player.state() == Phonon.PlayingState:
            seek = (val * self.player.totalTime()) / 100
            self.player.seek(seek)
            self.timeScratched.emit(seek)
        else:
            print "not playing... ", time
            
    def tick(self, time):
        ''' tick timer for player updates'''
        #print "Player::tick: ", time
        self._updateLabels()

    
    def _updateLabels(self):
        cur_s = 0
        total_s = 0
        if self.player and self.player.state() == Phonon.PlayingState:
            cur_s = self.player.currentTime() / 1000.
            self.timeStart.emit(handle_time(cur_s))
            total_s = self.player.totalTime() / 1000.
            self.timeTotal.emit(handle_time(total_s))
        

    def finished(self):
        print "Player::finished"

def handle_time(time):
        m, s = divmod(time, 60)
        if m < 60:
            return "%02i:%02i" % (m, s)
        else:
            h, m = divmod(m, 60)
            return "%i:%02i:%02i" % (h, m, s)
        
def show_msg(self, msg):
    '''
        simple message box
    '''
    msgbox = QtGui.QMessageBox()
    msgbox.setText(msg)
    msgbox.exec_()
        
def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('pymp')
    pympgui = PympGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
