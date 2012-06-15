from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.phonon import Phonon
from .logger import init_logger
from .utils import handle_time

logger = init_logger()


class Player(QObject):
    '''
        Handle for the Phonon class
    '''
    # tick for player
    timeStart = pyqtSignal(QString)
    timeTotal = pyqtSignal(QString)
    sldMove = pyqtSignal(int)
    timeScratched = pyqtSignal(int)
    volScratched = pyqtSignal(int)
    finishedSong = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self.player = Phonon.MediaObject(self)
        self.m_audio = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.player, self.m_audio)
        self.player.setTickInterval(100)
        # actions
        self.player.tick.connect(self.tick)
        self.player.finished.connect(self.finished)

        #print Phonon.BackendCapabilities.availableAudioEffects()
        # QSlider -> SeekSlider
        #self.slider_time = Phonon.SeekSlider(self.player, self)

    def tick(self):
        self._update_labels()

    def play(self, cpath):
        self.player.setCurrentSource(Phonon.MediaSource(cpath))
        self.player.play()

    def stop(self):
        self.player.stop()

    def nxt(self, cpath):
        logger.info("Player::next")

    def prev(self):
        logger.info("Player::prev")

    def mute(self):
        self.m_audio.setMuted(not self.m_audio.isMuted())
        logger.info("muted: {}".format(self.m_audio.isMuted()))

    def random(self):
        logger.info("Player::random")

    def repeat(self):
        logger.info("Player::repeat")

    def volume(self, val):
        ''' TODO: slider changed value'''
        self.volScratched.emit(val)
        val = float(val) / 100.
        #print dir(self.m_audio)
        self.m_audio.setVolume(val)

    def time(self, val):
        ''' TODO: slider changed value'''
        if self.player and self.player.state() == Phonon.PlayingState:
            seek = (val * self.player.totalTime()) / 100
            self.player.seek(seek)
            self.timeScratched.emit(seek)
        else:
            logger.info("not playing... {}".format(val))

    def _update_labels(self):
        cur_s = 0
        total_s = 0
        if self.player and self.player.state() == Phonon.PlayingState:
            cur_s = self.player.currentTime() / 1000.
            self.timeStart.emit(handle_time(cur_s))
            total_s = self.player.totalTime() / 1000.
            self.timeTotal.emit(handle_time(total_s))
            sld_val = cur_s / total_s * 100
            self.sldMove.emit(sld_val)

    def finished(self):
        self.finishedSong.emit()
