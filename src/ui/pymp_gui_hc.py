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
#from PyQt4.QtCore import Qt, QSize, QTimer
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from tree_model import myModel
from table_model import MyTableModel
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
        self.menuMap = {}
        
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
        actionsDict = {
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
                         'shuffle' :    ['shuffle', 'Ctrl+F', 'shuffle true/false', self.defAction, iconset['random_f']],
                         'repeat' :    ['repeat', 'Ctrl+F', 'repeat true/false', self.defAction, iconset['repeat_f']],
                         'clear' :    ['clear Playlist', 'Ctrl+F', 'clear playlist', self.defAction, iconset['clear']],
                         'help' :           ['help', 'Ctrl+F', 'help', QtGui.qApp.quit, iconset['cancel']],
                         'about' :          ['About pymp', 'Ctrl+F', 'about', QtGui.qApp.quit, iconset['cancel']],
                         'exit' :           ['Exit', 'Ctrl+Q', 'Exit Application', QtGui.qApp.quit, iconset['exit']],
                         }
        
        # compute actions-dict
        for (k,v) in actionsDict.items():
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
        [self.toolbar.addAction(self.actions[_]) for _ in actionsDict.keys()]
        
        self.setGeometry(20, 20, 1220, 620)
        self.setWindowTitle('pymp')
        
        controlBar = ControlBar(self)
        searchBarCollection = SearchBar(self)
        searchBarPlaylist = SearchBar(self)
        plsPanel = PlaylistPanel(self)
        colPanel = CollectionPanel(self, plsPanel)
        trackInfo = TrackInfoBar(self)
        lyricPanel = LyricPanel(self)
        lyricPanel.search('Skindred', 'Stand for Something')
        
        mainpanel = QtGui.QWidget(self)
        hbox = QtGui.QHBoxLayout(mainpanel)
        hbox.setSpacing(0)
        vboxCollection = QtGui.QVBoxLayout(mainpanel)
        vboxCollection.addWidget(searchBarCollection)
        vboxCollection.addWidget(colPanel, 1)
        
        vboxPlaylist = QtGui.QVBoxLayout(mainpanel)
        
        vboxPlaylist.addWidget(searchBarPlaylist)
        vboxPlaylist.addWidget(plsPanel, 1)
        vboxPlaylist.addWidget(trackInfo)
        vboxPlaylist.addWidget(controlBar)
        
        vboxLyric = QtGui.QVBoxLayout(mainpanel)
        vboxLyric.addWidget(lyricPanel, 1)
        
        hbox.addLayout(vboxCollection)
        hbox.addLayout(vboxPlaylist, 1)
        hbox.addLayout(vboxLyric)
        
        self.setCentralWidget(mainpanel)
        mainpanel.setLayout(hbox)
        
        trackInfo.track("Skindred", "Stand for Something", "Shark Bites and Dog Fights", "2009", "01", "Reggae-Metal")
        lyricPanel.search("Skindred", "Stand for Something")
        
        #id3dlg = ID3Edit(self, '../skindred/01 - Stand For Something.mp3')
        #id3dlg.show()
        self.show()
    
    def defAction(self):
        print "TODO"
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


class PlaylistPanel(QtGui.QWidget):
    '''
        Playlist Table
        
        click
        dclick
        
    '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
    
    def initUI(self):
        ''' TODO: init user interface '''
        self.tbl = QtGui.QTableView(self)
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
        vh = self.tbl.verticalHeader()
        vh.setVisible(False)
        hh = self.tbl.horizontalHeader()
        hh.setStretchLastSection(True)
        
        vbox = QtGui.QHBoxLayout(self)
        vbox.addWidget(self.tbl, 1)
        self.tbl.clicked.connect(self.clicked)
        self.tbl.doubleClicked.connect(self.double_clicked)
        self.tbl.activated.connect(self.activated)
        self.tbl.entered.connect(self.entered)
        self.tbl.pressed.connect(self.pressed)
    
    def clicked(self, idx):
        print 'playlist_clicked: ', idx
        data = self.model.data_row(idx.row())
        self.current_path = '%s' % data[len(data)-1]
        #print "current_path: ", type(self.current_path)
        
    def double_clicked(self):
        print "playlist::double_clicked"
        raise NotImplementedError
    def activated(self):
        print "playlist::activated"
        raise NotImplementedError
    def entered(self):
        print "playlist::entered"
        raise NotImplementedError
    def pressed(self):
        print "playlist::pressed"
        raise NotImplementedError
    def append(self, item):
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
        self.tre.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tre.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tre.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tre.customContextMenuRequested.connect(self.popup)
        self.tre.clicked.connect(self.clicked)
        self.tre.activated.connect(self.activated)
        self.tre.pressed.connect(self.pressed)
        
        self._dclick_timer.timeout.connect(self._dclick_timeout)
     
        vbox = QtGui.QHBoxLayout(self)
        vbox.addWidget(self.tre, 1)
    
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

    def activated(self):
        print "activated"
        raise NotImplementedError
    def pressed(self):
        print "pressed"
        raise NotImplementedError
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
        self.initUI()
    
    def initUI(self):
        self.txt = QtGui.QTextEdit(self)
        self.txt.setReadOnly(True)
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.txt)
         
    def search(self, artist, track):
        monkey = LyricWorker("Skindred", "Stand for Something")
        self.connect(monkey, QtCore.SIGNAL('update(QString)'), self.txt, QtCore.SIGNAL('setText(QString)'))
        #monkey.start()
    
    #@pyqtSlot('QString')
    def lyricChanged(self, lyr):
        print "called lyricChanged"
        self.txt.setText(lyr)


class LyricWorker(QtCore.QThread):
    def __init__(self, artist, title):
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
            print "Lyric: ", lyr
            #self.emit(QtCore.SIGNAL('update(QString)'), lyr)
        else:
            print "QThread filed?..."
        return
    
    def _read(self):
        fp = os.path.join(PYMPCFG[LYRICS_DIR], "%s-%s.txt" % (self.artist, self.title))
        try:
            with open(fp, 'r') as f:
                lyr = f.read()
            return lyr
        except Exception, e:
            print("Lyrics Datei nicht gefunden: %s" % (fp))
        return ''

    def _save(self, lyr):
        fp = os.path.join(PYMPCFG[LYRICS_DIR], "%s-%s.txt" % (self.artist, self.title))
        with open(fp, 'w') as f:
            f.write(lyr.encode('utf-8'))


class TrackInfoBar(QtGui.QWidget):
    '''
        Track Information Panel with current track
    '''
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
        self.lineArtist = QtGui.QLabel("artist", self)
        self.lineTitel = QtGui.QLabel("titel", self)
        self.lineAlbum = QtGui.QLabel("album", self)
        self.lineYear = QtGui.QLabel("year", self)
        self.lineTracknr = QtGui.QLabel("tracknr", self)
        self.lineGenre = QtGui.QLabel("genre", self)
        
        vbox = QtGui.QVBoxLayout(self)
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(self.lineArtist)
        hbox.addWidget(self.lineTitel)
        vbox.addLayout(hbox)
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(self.lineAlbum)
        hbox.addWidget(self.lineYear)
        hbox.addWidget(self.lineTracknr)
        hbox.addWidget(self.lineGenre)
        vbox.addLayout(hbox)
        
    
    def track(self, artist, title, album, year, tracknr, genre):
        '''
            fill fields with data
        '''
        self.artist = artist
        self.title = title
        self.album = album
        self.year = year
        self.tracknr = tracknr
        self.genre = genre
        self.updateInformation()
    
    def updateInformation(self):
        '''
            sync vars with gui-labels
        '''
        self.lineArtist.setText(self.artist)
        self.lineTitel.setText(self.title)
        self.lineAlbum.setText(self.album)
        self.lineYear.setText(self.year)
        self.lineTracknr.setText(self.tracknr)
        self.lineGenre.setText(self.genre)


class SearchBar(QtGui.QWidget):
    '''
        Control Panel for search patterns
    '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
    def initUI(self):
        ''' TODO: init user interface '''
        #pref = '../data/'
        #cssButton = "border-style: flat; border-width: 0px; border-color: black;"
        clr = QtGui.QPushButton(QtGui.QIcon(iconset['cancel']), "", self)
        clr.setFocusPolicy(QtCore.Qt.NoFocus)
        clr.clicked.connect(self.clrSearch)
        clr.setMinimumSize(QtCore.QSize(32,32))
        #clr.setStyleSheet(cssButton)
        
        self.line = QtGui.QLineEdit('', self)
        self.line.textChanged.connect(self.txChanged)
        self.line.returnPressed.connect(self.txReturn)
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(clr)
        hbox.addWidget(self.line, 1)
    
    def txChanged(self, t):
        print "txChanged ", t
        raise NotImplementedError
    
    def txReturn(self):
        print "pattern: ", self.line.text()
        raise NotImplementedError
    
    def clrSearch(self):
        ''' clear search '''
        self.line.setText('')


class ControlBar(QtGui.QWidget):
    '''
        Control Panel for prev, play, stop, next, mute and volume
    '''
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
        prev.clicked.connect(self.onPrev)
        prev.setMinimumSize(sze)
        prev.setMaximumSize(sze)
        #prev.setStyleSheet(cssButton)
        
        stop = QtGui.QPushButton(QtGui.QIcon(iconset['playback_stop']), "", self)
        stop.setFocusPolicy(QtCore.Qt.NoFocus)
        stop.clicked.connect(self.onStop)
        stop.setMinimumSize(sze)
        stop.setMaximumSize(sze)
        #stop.setStyleSheet(cssButton)
        
        play = QtGui.QPushButton(QtGui.QIcon(iconset['playback_play']), "", self)
        play.setFocusPolicy(QtCore.Qt.NoFocus)
        play.clicked.connect(self.onPlay)
        play.setMinimumSize(sze)
        play.setMaximumSize(sze)
        #play.setStyleSheet(cssButton)
        
        nxt = QtGui.QPushButton(QtGui.QIcon(iconset['playback_next']), "", self)
        nxt.setFocusPolicy(QtCore.Qt.NoFocus)
        nxt.clicked.connect(self.onNext)
        nxt.setMinimumSize(sze)
        nxt.setMaximumSize(sze)
        #nxt.setStyleSheet(cssButton)
        
        mute = QtGui.QPushButton(QtGui.QIcon(iconset['playback_mute']), "", self)
        mute.setFocusPolicy(QtCore.Qt.NoFocus)
        mute.clicked.connect(self.onMute)
        mute.setMinimumSize(sze)
        mute.setMaximumSize(sze)
        #mute.setStyleSheet(cssButton)
        
        sldVol = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sldVol.setFocusPolicy(QtCore.Qt.NoFocus)
        sldVol.valueChanged[int].connect(self.volChangeValue)
        
        tstart = QtGui.QLabel("00:00", self)
        
        sldTime = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sldTime.setFocusPolicy(QtCore.Qt.NoFocus)
        sldTime.valueChanged[int].connect(self.timeChangeValue)
        
        tremain = QtGui.QLabel("23:59", self)
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(prev, 0)
        hbox.addWidget(stop, 0)
        hbox.addWidget(play)
        hbox.addWidget(nxt)
        hbox.addWidget(mute)
        hbox.addWidget(sldVol)
        hbox.addWidget(tstart)
        hbox.addWidget(sldTime, 1)
        hbox.addWidget(tremain)
    
    def onPrev(self):
        ''' TODO: pressed prev'''
        print "pressed prev"
        raise NotImplementedError
        
    def onStop(self):
        ''' TODO: pressed stop'''
        print "pressed stop"
        raise NotImplementedError
        
    def onPlay(self):
        ''' TODO: pressed play'''
        print "pressed play"
        raise NotImplementedError
        
    def onNext(self):
        ''' TODO: pressed next'''
        print "pressed next"
        raise NotImplementedError
        
    def onMute(self):
        ''' TODO: pressed mute'''
        print "pressed mute"
        raise NotImplementedError
        
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
        
def show_msg(self, msg):
    '''
        simple message box
    '''
    msgbox = QtGui.QMessageBox()
    msgbox.setText(msg)
    msgbox.exec_()
        
def main():
    app = QtGui.QApplication(sys.argv)
    pympgui = PympGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
