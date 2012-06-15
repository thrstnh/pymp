from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .style import iconset
from .player import Player
from .ui.control import ControlBar
from .ui.playlist import PlaylistPanel
from .ui.collection import CollectionPanel
from .ui.lyric import LyricPanel
from .ui.trackinfo import TrackInfoBar
from .ui.search import SearchBar
from .ui.queue import QueueDialog
from .logger import init_logger

logger = init_logger()


class PympGUI(QMainWindow):

    def __init__(self):
        super(PympGUI, self).__init__()

        self.actions = {}
        self.uistyles = [str(style) for style in QStyleFactory.keys()]
        self.uistyleid = 0
        QApplication.setStyle(QStyleFactory.create(self.uistyles[self.uistyleid]))
        QApplication.setPalette(QApplication.style().standardPalette())
        cssStyle = '''QWidget {
                border: 0px solid black;
                padding: 0px;
                margin: 0px;}
        '''
#        self.setStyleSheet(cssStyle)
        self.queuedlg = QueueDialog(self)
        self.initUI()

    def initUI(self):
        # actions in a dict :)
        self.actionsDict = {
                         'addCollection':  ['Add &Collection', 'Ctrl+Q', 'Add Collection',
                                            qApp.quit,
                                            iconset['new']],
                         'newPlaylist':    ['New &Playlist', 'Ctrl+P', 'New Playlist',
                                            qApp.quit,
                                            iconset['new']],
                         'openPlaylist':   ['Open Playlist', 'Ctrl+P', 'Open Playlist',
                                            qApp.quit,
                                            iconset['open']],
                         'savePlaylist':   ['Save Playlist', 'Ctrl+P', 'Save Playlist',
                                            qApp.quit,
                                            iconset['save']],
                         'viewCollection': ['View Collection', 'Ctrl+I', 'View Collection Panel',
                                            qApp.quit,
                                            iconset['cancel']],
                         'viewLyric':      ['View Lyric', 'Ctrl+L', 'View Lyric Panel',
                                            qApp.quit,
                                            iconset['cancel']],
                         # ctrl actions
                         'playback_ff':    ['FF', 'Ctrl+Q', 'Forward',
                                            qApp.quit,
                                            iconset['playback_ff']],
                         'playback_next':  ['Next', 'Ctrl+Q', 'Next Track',
                                            qApp.quit,
                                            iconset['playback_next']],
                         'playback_pause': ['Pause', 'Ctrl+Q', 'Pause',
                                            qApp.quit,
                                            iconset['playback_pause']],
                         'playback_play':  ['Play', 'Ctrl+Q', 'Play',
                                            qApp.quit,
                                            iconset['playback_play']],
                         'playback_prev':  ['Prev', 'Ctrl+Q', 'Prev',
                                            qApp.quit,
                                            iconset['playback_prev']],
                         'playback_rew':   ['Rew', 'Ctrl+Q', 'Rew',
                                            qApp.quit,
                                            iconset['playback_rew']],
                         'playback_stop':  ['Stop', 'Ctrl+Q', 'Stop',
                                            qApp.quit,
                                            iconset['playback_stop']],
                         'playback_mute':  ['Mute', 'Ctrl+Q', 'Mute',
                                            qApp.quit,
                                            iconset['playback_mute']],
                         'lookandfeel':    ['look and feel', 'Ctrl+F', 'Change look and feel',
                                            self.lookandfeel,
                                            iconset['lookandfeel']],
                         'shuffle':        ['shuffle', 'Ctrl+F', 'shuffle true/false',
                                            self.defAction,
                                            iconset['random_f']],
                         'repeat':         ['repeat', 'Ctrl+F', 'repeat true/false',
                                            self.defAction,
                                            iconset['repeat_f']],
                         'clear':          ['clear Playlist', 'Ctrl+F', 'clear playlist',
                                            self.defAction,
                                            iconset['clear']],
                         'help':           ['help', 'Ctrl+F', 'help',
                                            qApp.quit,
                                            iconset['cancel']],
                         'about':          ['About pymp', 'Ctrl+F', 'about',
                                            qApp.quit,
                                            iconset['cancel']],
                         'exit':           ['Exit', 'Ctrl+Q', 'Exit Application',
                                            qApp.quit,
                                            iconset['exit']]}

        # compute actions-dict
        for (k,v) in self.actionsDict.items():
            (_name, _shortcut, _statustip, _action, _icon) = v
            self.actions[k] = self.qtregister_action(_name, _shortcut, _statustip, _action, _icon)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        viewMenu = menubar.addMenu('&View')
        playbackMenu = menubar.addMenu('&Playback')
        helpMenu = menubar.addMenu('&Help')
        [fileMenu.addAction(self.actions[k])
                for k in ['addCollection',
                          'newPlaylist',
                          'openPlaylist',
                          'savePlaylist',
                          'exit']]
        [viewMenu.addAction(self.actions[k])
                for k in ['help',
                          'viewLyric',
                          'lookandfeel']]
        [playbackMenu.addAction(self.actions[k])
                for k in ['shuffle']]
        [helpMenu.addAction(self.actions[k])
                for k in ['viewCollection',
                          'about']]

        self.statusBar()
        self.statusBar().showMessage('Ready')

        self.setGeometry(20, 20, 1220, 620)
        self.setWindowTitle('pymp')

        self.left = QFrame(self)
        self.left.setFrameShape(QFrame.StyledPanel)

        self.center = QFrame(self)
        self.center.setFrameShape(QFrame.StyledPanel)
        self.right = QFrame(self)
        self.right.setFrameShape(QFrame.StyledPanel)

        splitterMain = QSplitter(Qt.Horizontal)

        # controls
        self.controlBar = ControlBar(self)
        self.searchBarCollection = SearchBar(self)
        self.searchBarPlaylist = SearchBar(self)
        self.plsPanel = PlaylistPanel(self)
        self.colPanel = CollectionPanel(self, self.plsPanel)
        self.trackInfo = TrackInfoBar(self)
        self.lyricPanel = LyricPanel(self)

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        vboxCollection = QVBoxLayout(self)
        vboxCollection.addWidget(self.searchBarCollection)
        vboxCollection.addWidget(self.colPanel, 1)
        self.left.setLayout(vboxCollection)

        vboxPlaylist = QVBoxLayout(self)
        vboxPlaylist.addWidget(self.searchBarPlaylist)
        vboxPlaylist.addWidget(self.plsPanel, 1)
        vboxPlaylist.addWidget(self.trackInfo)
        self.center.setLayout(vboxPlaylist)

        vboxLyric = QVBoxLayout(self)
        vboxLyric.addWidget(self.lyricPanel, 1)
        self.right.setLayout(vboxLyric)
        self.right.setVisible(False)

        splitterMain.addWidget(self.left)
        splitterMain.addWidget(self.center)
        splitterMain.addWidget(self.right)

        splitterMain.setStretchFactor(0, 1)
        splitterMain.setStretchFactor(1, 2)
        splitterMain.setStretchFactor(2, 1)

        vbox = QVBoxLayout(self)
        vbox.addWidget(splitterMain, 1)
        vbox.addWidget(self.controlBar)

        layout = QFrame(self)
        layout.setLayout(vbox)
        self.setCentralWidget(layout)
        self.show()

    def toggleCollection(self):
        self.left.setVisible(not self.left.isVisible())

    def toggleLyric(self):
        self.right.setVisible(not self.right.isVisible())

    def defAction(self):
        raise NotImplementedError

    def qtregister_action(self, name, shortcut, statustip, triggeraction, image):
        ''' TODO: register a qt-action the lazy way'''
        action = QAction(QIcon(image), name, self)
        action.setShortcut(shortcut)
        action.setStatusTip(statustip)
        action.triggered.connect(triggeraction)
        return action

    def lookandfeel(self):
        if self.uistyleid >= len(self.uistyles)-1:
            self.uistyleid = 0
        else:
            self.uistyleid += 1
        QApplication.setStyle(QStyleFactory.create(self.uistyles[self.uistyleid]))
        QApplication.setPalette(QApplication.style().standardPalette())

    def update_labels(self):
        logger.info('update labels')

    def showEvent(self, arg1):
        ''' show user interface '''
        # NOW init player, after gui shows up
        self.player = Player(self)
        # connect some actions
        self.controlBar.togCollection.connect(self.toggleCollection)
        self.controlBar.togLyric.connect(self.toggleLyric)
        self.controlBar.onPrev.connect(self.player.prev)
        self.controlBar.onStop.connect(self.player.stop)
        self.controlBar.onPlay.connect(self.player.play)
        self.controlBar.onNext.connect(self.plsPanel.nextPath)
        self.controlBar.onMute.connect(self.player.mute)
        self.controlBar.onVolume.connect(self.player.volume)
        self.controlBar.onTime.connect(self.player.time)
        self.controlBar.clearPlaylist.connect(self.plsPanel.clearPlaylist)
        self.plsPanel.playCurrent.connect(self.player.play)
        self.plsPanel.playCurrent.connect(self.trackInfo.update)
        self.plsPanel.playNext.connect(self.player.play)
        self.plsPanel.playNext.connect(self.trackInfo.update)
        self.player.timeStart.connect(self.controlBar.setTimeStart)
        self.player.timeTotal.connect(self.controlBar.setTimeTotal)
        self.player.sldMove.connect(self.controlBar.set_time)
        self.player.timeScratched.connect(self.controlBar.timeChangeValue)
        self.player.volScratched.connect(self.controlBar.volChangeValue)
        self.trackInfo.fetchLyrics.connect(self.lyricPanel.search)
        self.searchBarPlaylist.timerExpired.connect(self.plsPanel.usePattern)
        self.searchBarPlaylist.clearSearch.connect(self.plsPanel.usePattern)
        self.searchBarCollection.timerExpired.connect(self.colPanel.usePattern)
        self.searchBarCollection.clearSearch.connect(self.colPanel.usePattern)
        # IF REPEAT...
        self.player.finishedSong.connect(self.plsPanel.nextPath)
        #self.searchBarPlaylist.search.connect(self.plsPanel.usePattern)
        self.plsPanel.enqueue.connect(self.queuedlg.append)
        self.controlBar.set_volume(75)  # TODO read from config
