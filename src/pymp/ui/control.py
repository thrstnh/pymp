from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .widgets import BaseButton, ToggleButton
from ..logger import init_logger
from ..style import iconset
from ..config import init_env

logger = init_logger()
PYMPENV = init_env()


class ControlBar(QWidget):
    '''
        Control Panel for prev, play, stop, next, mute and volume
    '''
    # some new slots
    onPrev = pyqtSignal()
    onStop = pyqtSignal()
    onPlay = pyqtSignal()
    onNext = pyqtSignal()
    onPlay = pyqtSignal()
    onVolume = pyqtSignal(int)
    onTime = pyqtSignal(int)
    onShuffle = pyqtSignal()
    onFocus = pyqtSignal()
    togFocus = pyqtSignal()
    togLyric = pyqtSignal()
    togCollection = pyqtSignal()
    togMute = pyqtSignal()
    togRandom = pyqtSignal()
    togRepeat = pyqtSignal()
    clearPlaylist = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):
        togC = ToggleButton(PYMPENV['SHOW_COLLECTION'], self.togCollection.emit,
                            iconset['layout_lm'], iconset['layout_lp'])
        togL = ToggleButton(PYMPENV['SHOW_LYRIC'], self.togLyric.emit,
                            iconset['layout_rm'], iconset['layout_rp'])
        prev = BaseButton(self.onPrev.emit, iconset['playback_rew'])
        stop = BaseButton(self.onStop.emit, iconset['playback_stop'])
        play = BaseButton(self.onPlay.emit, iconset['playback_play'])
        nxt = BaseButton(self.onNext.emit, iconset['playback_next'])
        shuffle = BaseButton(self.onShuffle.emit, iconset['shuffle'])
        focus = BaseButton(self.onFocus.emit, iconset['search'])
        auto_focus = ToggleButton(PYMPENV['AUTO_FOCUS'], self.togFocus.emit,
                            iconset['focus_t'], iconset['focus_f'])
        random = ToggleButton(PYMPENV['RANDOM'], self.togRandom.emit,
                            iconset['random_t'], iconset['random_f'])
        repeat = ToggleButton(PYMPENV['REPEAT'], self.togRepeat.emit,
                            iconset['repeat_t'], iconset['repeat_f'])
        mute = ToggleButton(PYMPENV['MUTE'], self.togMute.emit,
                            iconset['playback_mute_t'], iconset['playback_mute'])

        self.sldVol = QSlider(Qt.Horizontal, self)
        self.sldVol.setFocusPolicy(Qt.NoFocus)
        self.sldVol.sliderMoved[int].connect(self.volChangeValue)
        self.sldVol.sliderMoved[int].connect(self.onVolume.emit)

        self.tstart = QLabel("00:00", self)

        self.sldTime = QSlider(Qt.Horizontal, self)
        self.sldTime.setFocusPolicy(Qt.NoFocus)
        self.sldTime.sliderMoved[int].connect(self.timeChangeValue)
        self.sldTime.sliderMoved[int].connect(self.onTime.emit)

        self.ttotal = QLabel("23:59", self)

        clr = BaseButton(self.clearPlaylist.emit, iconset['clear'])

        hbox = QHBoxLayout(self)
        hbox.addWidget(togC)
        hbox.addWidget(togL)
        hbox.addWidget(prev, 0)
        hbox.addWidget(stop, 0)
        hbox.addWidget(play)
        hbox.addWidget(nxt)
        hbox.addWidget(shuffle)
        hbox.addWidget(mute)
        hbox.addWidget(random)
        hbox.addWidget(repeat)
        hbox.addWidget(focus)
        hbox.addWidget(auto_focus)
        hbox.addWidget(self.sldVol)
        hbox.addWidget(self.tstart)
        hbox.addWidget(self.sldTime, 1)
        hbox.addWidget(self.ttotal)
        hbox.addWidget(clr)

    def setTimeStart(self, time):
        self.tstart.setText(time)

    def setTimeTotal(self, time):
        self.ttotal.setText(time)

    def set_volume(self, vol):
        self.sldVol.setValue(vol)

    def set_time(self, t):
        self.sldTime.setValue(t)

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
