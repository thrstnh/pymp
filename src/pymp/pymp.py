from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .style import iconset, css
from .player import Player
from .ui.control import ControlBar
from .ui.playlist import PlaylistPanel
from .ui.collection import CollectionPanel
from .ui.lyric import LyricPanel
from .ui.trackinfo import TrackInfoBar
from .ui.search import SearchBar
from .ui.queue import QueueDialog
from .logger import init_logger
from .config import init_env

logger = init_logger()
PYMPENV = init_env()


class PympGUI(QMainWindow):

    def __init__(self):
        super(PympGUI, self).__init__()
        self.__init_pymp_gui()
        self._init_styles()
        self._init_actions()
        self._compute_actions()
        self._init_menubar()
        self.setCentralWidget(self._init_ctrls())
        self.update_statusbar('Ready.')
        self.show()

    def __init_pymp_gui(self):
#        self.setStyleSheet(css)
        self.setWindowTitle('pymp')
        self.setWindowIcon(QIcon(iconset['pymp']))
        self.setGeometry(20, 20, 1220, 620)

    def _init_ctrls(self):
        self.queuedlg = QueueDialog(self)
        self.controlBar = ControlBar(self)
        self.plsPanel = PlaylistPanel(self)
        self.colPanel = CollectionPanel(self, self.plsPanel)
        self.searchBarCollection = SearchBar(self, iconset['delete'],
                                             PYMPENV['SEARCH_TIMEOUT'])
        self.searchBarPlaylist = SearchBar(self, iconset['delete'],
                                           PYMPENV['SEARCH_TIMEOUT'])
        self.trackInfo = TrackInfoBar(self)
        self.lyricPanel = LyricPanel(self)

        splitterMain = QSplitter(Qt.Horizontal)
        splitterMain.addWidget(self._init_ui_left())
        splitterMain.addWidget(self._init_ui_center())
        splitterMain.addWidget(self._init_ui_right())

        splitterMain.setStretchFactor(0, 1)
        splitterMain.setStretchFactor(1, 2)
        splitterMain.setStretchFactor(2, 1)

        vbox = QVBoxLayout(self)
        vbox.addWidget(splitterMain, 1)
        vbox.addWidget(self.controlBar)

        layout = QFrame(self)
        layout.setLayout(vbox)
        return layout

    def _init_ui_left(self):
        self.left = QFrame(self)
        self.left.setFrameShape(QFrame.StyledPanel)
        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        vboxCollection = QVBoxLayout(self)
        vboxCollection.addWidget(self.searchBarCollection)
        vboxCollection.addWidget(self.colPanel, 1)
        self.left.setLayout(vboxCollection)
        return self.left

    def _init_ui_center(self):
        self.center = QFrame(self)
        self.center.setFrameShape(QFrame.StyledPanel)
        vboxPlaylist = QVBoxLayout(self)
        vboxPlaylist.addWidget(self.searchBarPlaylist)
        vboxPlaylist.addWidget(self.plsPanel, 1)
        vboxPlaylist.addWidget(self.trackInfo)
        self.center.setLayout(vboxPlaylist)
        return self.center

    def _init_ui_right(self):
        self.right = QFrame(self)
        self.right.setFrameShape(QFrame.StyledPanel)
        vboxLyric = QVBoxLayout(self)
        vboxLyric.addWidget(self.lyricPanel, 1)
        self.right.setLayout(vboxLyric)
        self.right.setVisible(False)
        return self.right

    def _init_styles(self):
        self.uistyles = [str(style) for style in QStyleFactory.keys()]
        self.uistyleid = 0
        QApplication.setStyle(QStyleFactory.create(self.uistyles[self.uistyleid]))
        QApplication.setPalette(QApplication.style().standardPalette())

    def _init_actions(self):
        self.actions = {}
        # actions in a dict :)
        self.actionsDict = {
                'addCollection':  ['Add &Collection', 'Ctrl+Q', 'Add Collection',
                                    qApp.quit, iconset['new']],
                'newPlaylist':    ['New &Playlist', 'Ctrl+P', 'New Playlist',
                                    qApp.quit, iconset['new']],
                'openPlaylist':   ['Open Playlist', 'Ctrl+P', 'Open Playlist',
                                    qApp.quit, iconset['open']],
                'savePlaylist':   ['Save Playlist', 'Ctrl+P', 'Save Playlist',
                                    qApp.quit, iconset['save']],
                'viewCollection': ['View Collection', 'Ctrl+I', 'View Collection Panel',
                                    qApp.quit, iconset['cancel']],
                'viewLyric':      ['View Lyric', 'Ctrl+L', 'View Lyric Panel',
                                    qApp.quit, iconset['cancel']],
                # ctrl actions
                'playback_ff':    ['FF', 'Ctrl+Q', 'Forward',
                                    qApp.quit, iconset['playback_ff']],
                'playback_next':  ['Next', 'Ctrl+Q', 'Next Track',
                                    qApp.quit, iconset['playback_next']],
                'playback_pause': ['Pause', 'Ctrl+Q', 'Pause',
                                    qApp.quit, iconset['playback_pause']],
                'playback_play':  ['Play', 'Ctrl+Q', 'Play',
                                    qApp.quit, iconset['playback_play']],
                'playback_prev':  ['Prev', 'Ctrl+Q', 'Prev',
                                    qApp.quit, iconset['playback_prev']],
                'playback_rew':   ['Rew', 'Ctrl+Q', 'Rew',
                                    qApp.quit, iconset['playback_rew']],
                'playback_stop':  ['Stop', 'Ctrl+Q', 'Stop',
                                    qApp.quit, iconset['playback_stop']],
                'playback_mute':  ['Mute', 'Ctrl+Q', 'Mute',
                                    qApp.quit, iconset['playback_mute']],
                'lookandfeel':    ['look and feel', 'Ctrl+F', 'Change look and feel',
                                    self.lookandfeel, iconset['lookandfeel']],
                'shuffle':        ['shuffle', 'Ctrl+F', 'shuffle true/false',
                                    self.defAction, iconset['random_f']],
                'repeat':         ['repeat', 'Ctrl+F', 'repeat true/false',
                                    self.defAction, iconset['repeat_f']],
                'clear':          ['clear Playlist', 'Ctrl+F', 'clear playlist',
                                    self.defAction, iconset['clear']],
                'help':           ['help', 'Ctrl+F', 'help',
                                    qApp.quit, iconset['cancel']],
                'about':          ['About pymp', 'Ctrl+F', 'about',
                                    qApp.quit, iconset['cancel']],
                'exit':           ['Exit', 'Ctrl+Q', 'Exit Application',
                                    qApp.quit, iconset['exit']]}

    def _compute_actions(self):
        # compute actions-dict
        for (k,v) in self.actionsDict.items():
            (_name, _shortcut, _statustip, _action, _icon) = v
            self.actions[k] = self.qtregister_action(_name, _shortcut, _statustip, _action, _icon)

    def _init_menubar(self):
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

    def toggleCollection(self):
        self.left.setVisible(not self.left.isVisible())

    def toggleLyric(self):
        self.right.setVisible(not self.right.isVisible())
        if PYMPENV['CURRENT_TRACK']:
            self.lyricPanel.search(
                        str(PYMPENV['CURRENT_TRACK'].artist),
                        str(PYMPENV['CURRENT_TRACK'].title))

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

    def update_statusbar(self, msg=''):
        if not msg:
            msg = '{} tracks.'.format(self.plsPanel.model.length())
        logger.debug(':statusbar {}'.format(msg))
        self.statusBar().showMessage(msg)

    def _handle_random(self):
        PYMPENV.toggle('RANDOM')

    def _handle_repeat(self):
        PYMPENV.toggle('REPEAT')

    def _handle_auto_focus(self):
        PYMPENV.toggle('AUTO_FOCUS')

    def showEvent(self, arg1):
        ''' show user interface '''
        # NOW init player, after gui shows up
        self.player = Player(self)
        # connect some actions
        self.controlBar.togCollection.connect(self.toggleCollection)
        self.controlBar.togRandom.connect(self._handle_random)
        self.controlBar.togRepeat.connect(self._handle_repeat)
        self.controlBar.togLyric.connect(self.toggleLyric)
        self.controlBar.onPrev.connect(self.plsPanel.prev_path)
        self.controlBar.onPrev.connect(self.trackInfo.update_env)
        self.controlBar.onStop.connect(self.player.stop)
        self.controlBar.onStop.connect(self.trackInfo.update_env)
        self.controlBar.onPlay.connect(self.plsPanel.current_path)
        self.controlBar.onPlay.connect(self.trackInfo.update_env)
        self.controlBar.onNext.connect(self.plsPanel.next_path)
        self.controlBar.onNext.connect(self.trackInfo.update_env)
        self.controlBar.onShuffle.connect(self.plsPanel.model.shuffle)
        self.controlBar.togMute.connect(self.player.mute)
        self.controlBar.onVolume.connect(self.player.volume)
        self.controlBar.onTime.connect(self.player.time)
        self.controlBar.clearPlaylist.connect(self.plsPanel.clearPlaylist)
        self.controlBar.togFocus.connect(self._handle_auto_focus)
        self.plsPanel.playCurrent.connect(self.player.play)
        self.plsPanel.playCurrent.connect(self.trackInfo.update)
        self.plsPanel.playNext.connect(self.player.play)
        self.plsPanel.playNext.connect(self.trackInfo.update)
        self.plsPanel.playPrev.connect(self.player.play)
        self.plsPanel.playPrev.connect(self.trackInfo.update)
        self.player.timeStart.connect(self.controlBar.setTimeStart)
        self.player.timeTotal.connect(self.controlBar.setTimeTotal)
        self.player.sldMove.connect(self.controlBar.set_time)
        self.player.timeScratched.connect(self.controlBar.timeChangeValue)
        self.player.volScratched.connect(self.controlBar.volChangeValue)
        self.trackInfo.fetchLyrics.connect(self.lyricPanel.search)
        self.searchBarPlaylist.clearSearch.connect(self.plsPanel.search)
        self.searchBarPlaylist.timerExpired.connect(self.plsPanel.search)
        self.searchBarCollection.timerExpired.connect(self.colPanel.usePattern)
        self.searchBarCollection.clearSearch.connect(self.colPanel.usePattern)
        # IF REPEAT...
        self.player.finishedSong.connect(self.plsPanel.next_path)
        #self.searchBarPlaylist.search.connect(self.plsPanel.usePattern)
        self.plsPanel.enqueue.connect(self.queuedlg.append)
