#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author: thrstnh
email:  thrstn.hllbrnd@googlemail.com
date:   07.12.2011 16:15
"""
import sys
from PyQt4.QtCore import Qt, QSize
from PyQt4 import QtGui
from collections import OrderedDict
from PyQt4.QtCore import QRect


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
                         'addCollection' :  ['Add &Collection', 'Ctrl+Q', 'Add Collection', QtGui.qApp.quit, 'exit.png'],
                         'newPlaylist' :    ['New &Playlist', 'Ctrl+P', 'New Playlist', QtGui.qApp.quit, 'exit.png'],
                         'openPlaylist' :   ['Open Playlist', 'Ctrl+P', 'Open Playlist', QtGui.qApp.quit, 'exit.png'],
                         'savePlaylist' :   ['Save Playlist', 'Ctrl+P', 'Save Playlist', QtGui.qApp.quit, 'exit.png'],
                         'exit' :           ['Exit', 'Ctrl+Q', 'Exit Application', QtGui.qApp.quit, 'exit.png'],
                         'viewCollection' : ['View Collection', 'Ctrl+I', 'View Collection Panel', QtGui.qApp.quit, 'exit.png'],
                         'viewLyric' :      ['View Lyric', 'Ctrl+L', 'View Lyric Panel', QtGui.qApp.quit, 'exit.png'],
                         'lookandfeel' :    ['look and feel', 'Ctrl+F', 'Change look and feel', QtGui.qApp.quit, 'exit.png'],
                         'help' :           ['help', 'Ctrl+F', 'help', QtGui.qApp.quit, 'exit.png'],
                         'about' :          ['about pymp', 'Ctrl+F', 'about', QtGui.qApp.quit, 'exit.png'],
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
        
        #vbox = QtGui.QVBoxLayout()
        self.controlBar = ControlBar(self)
        #self.setLayout(vbox)
        
        self.show()
    

    def qtregister_action(self, name, shortcut, statustip, triggeraction, image):
        ''' TODO: register a qt-action the lazy way'''
        action = QtGui.QAction(QtGui.QIcon(image), name, self)
        action.setShortcut(shortcut)
        action.setStatusTip(statustip)
        action.triggered.connect(triggeraction)
        return action


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
        
        cssButton = cssDEBUG
        
        self.setStyleSheet(cssDEBUG)
        
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
        
        next = QtGui.QPushButton(QtGui.QIcon(pref + 'control_fastforward.png'), "", self)
        next.setFocusPolicy(Qt.NoFocus)
        next.clicked.connect(self.onNext)
        next.setMinimumSize(QSize(32,32))
        next.setStyleSheet(cssButton)
        
        mute = QtGui.QPushButton(QtGui.QIcon(pref + 'mute.png'), "", self)
        mute.setFocusPolicy(Qt.NoFocus)
        mute.clicked.connect(self.onMute)
        mute.setMinimumSize(QSize(32,32))
        mute.setStyleSheet(cssButton)
        
        sld = QtGui.QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)
        
        hbox = QtGui.QHBoxLayout(self)
        #hbox.addStretch(1)
        hbox.addWidget(prev)
        hbox.addWidget(stop)
        hbox.addWidget(play)
        #self.layout().addWidget(play)
        hbox.addWidget(next)
        hbox.addWidget(mute)
        hbox.addWidget(sld)
        
        #vbox = QtGui.QVBoxLayout(self)
        #vbox.addStretch(1)
        #vbox.addLayout(hbox)
        #self.setLayout(hbox)
        #self.setPalette(QtGui.QPalette(QtGui.QPalette.Background, Qt.black))
               
        self.setGeometry(100, 100, 130+5*40, 40)
    
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
        
    def changeValue(self, value):
        ''' TODO: slider changed value'''
        print 'volume ',
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
        

def main():
    app = QtGui.QApplication(sys.argv)
    pympgui = PympGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
