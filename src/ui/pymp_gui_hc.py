#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author: thrstnh
email:  thrstn.hllbrnd@googlemail.com
date:   07.12.2011 16:15
"""
import sys
from PyQt4.QtCore import Qt, QSize, QTimer
from PyQt4 import QtGui
from tree_model import myModel
from table_model import MyTableModel


class PympGUI(QtGui.QMainWindow):
    '''
        MainWindow of the python music player (pymp)
    '''
    def __init__(self):
        super(PympGUI, self).__init__()
        
        self.actions = {}
        self.menuMap = {}
        self.initUI()

    def initUI(self):
        ''' TODO: init user interface'''
        # actions in a dict :)
        menuStructure = {
                         'addCollection' :  ['Add &Collection', 'Ctrl+Q', 'Add Collection', QtGui.qApp.quit, 'cancel.png'],
                         'newPlaylist' :    ['New &Playlist', 'Ctrl+P', 'New Playlist', QtGui.qApp.quit, 'cancel.png'],
                         'openPlaylist' :   ['Open Playlist', 'Ctrl+P', 'Open Playlist', QtGui.qApp.quit, 'icon_open.png'],
                         'savePlaylist' :   ['Save Playlist', 'Ctrl+P', 'Save Playlist', QtGui.qApp.quit, 'icon_save.png'],
                         'exit' :           ['Exit', 'Ctrl+Q', 'Exit Application', QtGui.qApp.quit, 'cancel.png'],
                         'viewCollection' : ['View Collection', 'Ctrl+I', 'View Collection Panel', QtGui.qApp.quit, 'cancel.png'],
                         'viewLyric' :      ['View Lyric', 'Ctrl+L', 'View Lyric Panel', QtGui.qApp.quit, 'cancel.png'],
                         'lookandfeel' :    ['look and feel', 'Ctrl+F', 'Change look and feel', QtGui.qApp.quit, 'cancel.png'],
                         'help' :           ['help', 'Ctrl+F', 'help', QtGui.qApp.quit, 'cancel.png'],
                         'about' :          ['about pymp', 'Ctrl+F', 'about', QtGui.qApp.quit, 'cancel.png'],
                         }
        
        # compute actions-dict
        for (k,v) in menuStructure.items():
            (_name, _shortcut, _statustip, _action, _icon) = v
            self.actions[k] = self.qtregister_action(_name, _shortcut, _statustip, _action, _icon)
        
        menubar = self.menuBar()    
        fileMenu = menubar.addMenu('&File')
        viewMenu = menubar.addMenu('&View')
        helpMenu = menubar.addMenu('&Help')
        [fileMenu.addAction(self.actions[k]) for k in ['addCollection', 'newPlaylist', 'openPlaylist', 'savePlaylist', 'exit']]
        [viewMenu.addAction(self.actions[k]) for k in ['help', 'viewLyric', 'lookandfeel']]
        [helpMenu.addAction(self.actions[k]) for k in ['viewCollection', 'about']]

        self.statusBar()
        self.statusBar().showMessage('Ready')
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.actions['exit'])
        
        self.setGeometry(20, 20, 820, 620)
        self.setWindowTitle('pymp')
        
        controlBar = ControlBar(self)
        searchBarCollection = SearchBar(self)
        searchBarPlaylist = SearchBar(self)
        plsPanel = PlaylistPanel(self)
        colPanel = CollectionPanel(self, plsPanel)
        trackInfo = TrackInfoBar(self)
        
        mainpanel = QtGui.QWidget(self)
        hbox = QtGui.QHBoxLayout(mainpanel)
        vboxCollection = QtGui.QVBoxLayout(mainpanel)
        vboxCollection.addWidget(searchBarCollection)
        vboxCollection.addWidget(colPanel,1)
        
        vboxPlaylist = QtGui.QVBoxLayout(mainpanel)
        vboxPlaylist.addWidget(trackInfo)
        vboxPlaylist.addWidget(controlBar)
        vboxPlaylist.addWidget(searchBarPlaylist)
        vboxPlaylist.addWidget(plsPanel,1)
        
        hbox.addLayout(vboxCollection)
        hbox.addLayout(vboxPlaylist)
        
        self.setCentralWidget(mainpanel)
        mainpanel.setLayout(hbox)
        
        trackInfo.track("Skindred", "Stand for Something", "Shark Bites and Dog Fights", "2009", "01", "Reggae-Metal")
        self.show()
    
    def qtregister_action(self, name, shortcut, statustip, triggeraction, image):
        ''' TODO: register a qt-action the lazy way'''
        pref = '../data/'
        action = QtGui.QAction(QtGui.QIcon(pref + image), name, self)
        action.setShortcut(shortcut)
        action.setStatusTip(statustip)
        action.triggered.connect(triggeraction)
        return action


class PlaylistPanel(QtGui.QWidget):
    '''
        Playlist Table
    '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
    
    def initUI(self):
        ''' TODO: init user interface '''
        self.tbl = QtGui.QTableView(self)
        self.tm = MyTableModel()
        self.tbl.setModel(self.tm)

        self.tbl.setShowGrid(False)

        vh = self.tbl.verticalHeader()
        vh.setVisible(False)

        hh = self.tbl.horizontalHeader()
        hh.setStretchLastSection(True)

        self.tbl.setColumnHidden(0, True)
        self.tbl.setColumnHidden(self.tm.column_length()-1, True)
        
        vbox = QtGui.QHBoxLayout(self)
        vbox.addWidget(self.tbl, 1)
        self.tbl.clicked.connect(self.clicked)
        self.tbl.doubleClicked.connect(self.double_clicked)
        self.tbl.activated.connect(self.activated)
        self.tbl.entered.connect(self.entered)
        self.tbl.pressed.connect(self.pressed)
    
    def clicked(self):
        print "playlist::clicked"
    def double_clicked(self):
        print "playlist::clicked"
    def activated(self):
        print "playlist::clicked"
    def entered(self):
        print "playlist::clicked"
    def pressed(self):
        print "playlist::clicked"
    def append(self, item):
        self.tm.append(item)


class CollectionPanel(QtGui.QWidget):
    '''
        Collection Tree
    '''
    def __init__(self, parent=None, playlist=None):
        QtGui.QWidget.__init__(self, parent)
        self.playlist = playlist
        self._dclick_timer = QTimer(self)
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
        self.tre.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tre.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tre.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tre.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tre.customContextMenuRequested.connect(self.popup)
        self.tre.clicked.connect(self.clicked)
        self.tre.activated.connect(self.activated)
        self.tre.pressed.connect(self.pressed)
        
        self._dclick_timer.timeout.connect(self._dclick_timeout)
     
        vbox = QtGui.QHBoxLayout(self)
        vbox.addWidget(self.tre, 1)
    
    def _dclick_timeout(self):
        print "single click"
        index = self.idx
        self.tre.setExpanded(index, not self.tre.isExpanded(index))
        self._dclick_timer.stop()
                        
    def clicked(self, index):
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
        if node.hasChildren():
            for child in node.children:
                if isinstance(child.data, list):
                    self.playlist.append(child.data)
                if child.hasChildren():
                    self._add_child_nodes(child)

    def activated(self):
        print "activated"
    def pressed(self):
        print "pressed"
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
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(self.lineArtist)
        hbox.addWidget(self.lineTitel)
        hbox.addWidget(self.lineAlbum)
        hbox.addWidget(self.lineYear)
        hbox.addWidget(self.lineTracknr)
        hbox.addWidget(self.lineGenre)
    
    def track(self, artist, title, album, year, tracknr, genre):
        self.artist = artist
        self.title = title
        self.album = album
        self.year = year
        self.tracknr = tracknr
        self.genre = genre
        self.updateInformation()
    
    def updateInformation(self):
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
        pref = '../data/'
        cssButton = "border-style: flat; border-width: 0px; border-color: black;"
        clr = QtGui.QPushButton(QtGui.QIcon(pref + 'cancel.png'), "", self)
        clr.setFocusPolicy(Qt.NoFocus)
        clr.clicked.connect(self.clrSearch)
        clr.setMinimumSize(QSize(32,32))
        clr.setStyleSheet(cssButton)
        
        self.line = QtGui.QLineEdit('', self)
        self.line.textChanged.connect(self.txChanged)
        self.line.returnPressed.connect(self.txReturn)
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(clr)
        hbox.addWidget(self.line, 1)
    
    def txChanged(self, t):
        print "txChanged ", t
    
    def txReturn(self):
        print "pattern: ", self.line.text()
    
    def clrSearch(self):
        ''' TODO: pressed clrSearch'''
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
        
        prev = QtGui.QPushButton(QtGui.QIcon(pref + 'control_rewind.png'), "", self)
        prev.setFocusPolicy(Qt.NoFocus)
        prev.clicked.connect(self.onPrev)
        prev.setMinimumSize(QSize(32,32))
        prev.setStyleSheet(cssButton)
        
        stop = QtGui.QPushButton(QtGui.QIcon(pref + 'control_stop.png'), "", self)
        stop.setFocusPolicy(Qt.NoFocus)
        stop.clicked.connect(self.onStop)
        stop.setMinimumSize(QSize(32,32))
        stop.setStyleSheet(cssButton)
        
        play = QtGui.QPushButton(QtGui.QIcon(pref + 'control_play.png'), "", self)
        play.setFocusPolicy(Qt.NoFocus)
        play.clicked.connect(self.onPlay)
        play.setMinimumSize(QSize(32,32))
        play.setStyleSheet(cssButton)
        
        nxt = QtGui.QPushButton(QtGui.QIcon(pref + 'control_fastforward.png'), "", self)
        nxt.setFocusPolicy(Qt.NoFocus)
        nxt.clicked.connect(self.onNext)
        nxt.setMinimumSize(QSize(32,32))
        nxt.setStyleSheet(cssButton)
        
        mute = QtGui.QPushButton(QtGui.QIcon(pref + 'mute.png'), "", self)
        mute.setFocusPolicy(Qt.NoFocus)
        mute.clicked.connect(self.onMute)
        mute.setMinimumSize(QSize(32,32))
        mute.setStyleSheet(cssButton)
        
        sldVol = QtGui.QSlider(Qt.Horizontal, self)
        sldVol.setFocusPolicy(Qt.NoFocus)
        sldVol.valueChanged[int].connect(self.volChangeValue)
        
        tstart = QtGui.QLabel("00:00", self)
        
        sldTime = QtGui.QSlider(Qt.Horizontal, self)
        sldTime.setFocusPolicy(Qt.NoFocus)
        sldTime.valueChanged[int].connect(self.timeChangeValue)
        
        tremain = QtGui.QLabel("23:59", self)
        
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(prev)
        hbox.addWidget(stop)
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
        
    def onStop(self):
        ''' TODO: pressed stop'''
        print "pressed stop"
        
    def onPlay(self):
        ''' TODO: pressed play'''
        print "pressed play"
        
    def onNext(self):
        ''' TODO: pressed next'''
        print "pressed next"
        
    def onMute(self):
        ''' TODO: pressed mute'''
        print "pressed mute"
        
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
        
def show_msg(self, msg):
    msgbox = QtGui.QMessageBox()
    msgbox.setText(msg)
    msgbox.exec_()
        
def main():
    app = QtGui.QApplication(sys.argv)
    pympgui = PympGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
