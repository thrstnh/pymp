from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.phonon import Phonon
from .logger import init_logger
from .utils import handle_time
from .mp3 import PMP3, DMP3
from .config import init_env

logger = init_logger()
PYMPENV = init_env()


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
        #self.player.setTickInterval(100)
        #self.player.tick.connect(self._update_labels)
        self.player.finished.connect(self.finished)

#    def tick(self):
#        self._update_labels()

    def play(self, cpath):
        if not cpath:
            return
        self.player.setCurrentSource(Phonon.MediaSource(cpath))
        PYMPENV['CURRENT_TRACK'] = PMP3(cpath)
        #PYMPENV['CURRENT_DMP3'] = DMP3(cpath)
        self.player.play()
        if PYMPENV['CURRENT_TRACK']:
            logger.info('now playing:\n{}'.format(
                    '\n'.join(['  {} -> {}'.format(k,v)
                        for k,v in PYMPENV['CURRENT_TRACK'].all().items()])))

    def stop(self):
        self.player.stop()
        PYMPENV['CURRENT_TRACK'] = None
        self._update_labels()

    def mute(self):
        self.m_audio.setMuted(not self.m_audio.isMuted())
        logger.info("muted: {}".format(self.m_audio.isMuted()))

    def volume(self, val):
        self.volScratched.emit(val)
        val = float(val) / 100.
        #print dir(self.m_audio)
        self.m_audio.setVolume(val)

    def time(self, val):
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
        else:
            self.timeStart.emit('')
            self.timeTotal.emit('')
            self.sldMove.emit(0)

    def finished(self):
        self.finishedSong.emit()
