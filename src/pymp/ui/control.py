from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ..logger import init_logger
from ..style import iconset

logger = init_logger()


class ControlBar(QWidget):
    '''
        Control Panel for prev, play, stop, next, mute and volume
    '''
    # some new slots
    onPrev = pyqtSignal()
    onStop = pyqtSignal()
    onPlay = pyqtSignal()
    onNext = pyqtSignal()
    onMute = pyqtSignal()
    onPlay = pyqtSignal()
    onVolume = pyqtSignal(int)
    onTime = pyqtSignal(int)
    togLyric = pyqtSignal()
    togCollection = pyqtSignal()
    clearPlaylist = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):
        ''' TODO: init user interface'''
        pref = '../data/'
        cssButton = "border-style: flat; border-width: 0px; border-color: black;"
        cssDEBUG = "background-color: black; border-style: flat; border-width: 0px; border-color: black;"

        #cssButton = cssDEBUG

        #self.setStyleSheet(cssDEBUG)

        sze = QSize(24, 24)

        togC = QPushButton(QIcon(iconset['layout_lp']), "", self)
        togC.setFocusPolicy(Qt.NoFocus)
        togC.clicked.connect(self.togCollection.emit)
        togC.setMinimumSize(sze)
        togC.setMaximumSize(sze)

        togL = QPushButton(QIcon(iconset['layout_rp']), "", self)
        togL.setFocusPolicy(Qt.NoFocus)
        togL.clicked.connect(self.togLyric.emit)
        togL.setMinimumSize(sze)
        togL.setMaximumSize(sze)

        prev = QPushButton(QIcon(iconset['playback_rew']), "", self)
        prev.setFocusPolicy(Qt.NoFocus)
        prev.clicked.connect(self.onPrev.emit)
        prev.setMinimumSize(sze)
        prev.setMaximumSize(sze)
        #prev.setStyleSheet(cssButton)

        stop = QPushButton(QIcon(iconset['playback_stop']), "", self)
        stop.setFocusPolicy(Qt.NoFocus)
        stop.clicked.connect(self.onStop.emit)
        stop.setMinimumSize(sze)
        stop.setMaximumSize(sze)
        #stop.setStyleSheet(cssButton)

        play = QPushButton(QIcon(iconset['playback_play']), "", self)
        play.setFocusPolicy(Qt.NoFocus)
        play.clicked.connect(self.onPlay.emit)
        play.setMinimumSize(sze)
        play.setMaximumSize(sze)
        #play.setStyleSheet(cssButton)

        nxt = QPushButton(QIcon(iconset['playback_next']), "", self)
        nxt.setFocusPolicy(Qt.NoFocus)
        nxt.clicked.connect(self.onNext.emit)
        nxt.setMinimumSize(sze)
        nxt.setMaximumSize(sze)
        #nxt.setStyleSheet(cssButton)

        mute = QPushButton(QIcon(iconset['playback_mute']), "", self)
        mute.setFocusPolicy(Qt.NoFocus)
        mute.clicked.connect(self.onMute.emit)
        mute.setMinimumSize(sze)
        mute.setMaximumSize(sze)
        #mute.setStyleSheet(cssButton)

        self.sldVol = QSlider(Qt.Horizontal, self)
        self.sldVol.setFocusPolicy(Qt.NoFocus)
        self.sldVol.valueChanged[int].connect(self.volChangeValue)
        self.sldVol.valueChanged[int].connect(self.onVolume.emit)

        self.tstart = QLabel("00:00", self)

        sldTime = QSlider(Qt.Horizontal, self)
        sldTime.setFocusPolicy(Qt.NoFocus)
        sldTime.valueChanged[int].connect(self.timeChangeValue)
        sldTime.valueChanged[int].connect(self.onTime.emit)

        self.ttotal = QLabel("23:59", self)

        clr = QPushButton(QIcon(iconset['clear']), "", self)
        clr.setFocusPolicy(Qt.NoFocus)
        clr.clicked.connect(self.clearPlaylist.emit)
        clr.setMinimumSize(sze)
        clr.setMaximumSize(sze)

        hbox = QHBoxLayout(self)
        hbox.addWidget(togC)
        hbox.addWidget(togL)
        hbox.addWidget(prev, 0)
        hbox.addWidget(stop, 0)
        hbox.addWidget(play)
        hbox.addWidget(nxt)
        hbox.addWidget(mute)
        hbox.addWidget(self.sldVol)
        hbox.addWidget(self.tstart)
        hbox.addWidget(sldTime, 1)
        hbox.addWidget(self.ttotal)
        hbox.addWidget(clr)

    def setTimeStart(self, time):
        self.tstart.setText(time)

    def setTimeTotal(self, time):
        self.ttotal.setText(time)

    def set_volume(self, vol):
        self.sldVol.setValue(vol)

    def volChangeValue(self, value):
        self._slider_changed('volume', value)

    def timeChangeValue(self, value):
        self._slider_changed('time', value)

    def _slider_changed(self, name, value):
        if value == 0:
            ret = 'min'
        elif value == 99:
            ret = 'max'
        else:
            ret = value
        logger.info('{} {}'.format(name, ret))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        #rect = QRect(0, 0, self.width(), self.height())
        #qp.drawText(rect, Qt.AlignCenter, "self.text()")
        qp.end()
