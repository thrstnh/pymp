from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ..config import init_env

PYMPENV = init_env()


class TrackInfoBar(QWidget):

    fetchLyrics = pyqtSignal(QString, QString)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._init()
        self._init_ui()

    def _init(self):
        self.track = dict()
        self.track['PATH'] = ''
        self.track['artist'] = ''
        self.track['title'] = ''
        self.track['album'] = ''
        self.track['year'] = ''
        self.track['tracknr'] = ''
        self.track['genre'] = ''

    def _init_ui(self):
        self.customLabel = QLabel(self)
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.customLabel)
        vbox.addLayout(hbox)

    def update_env(self):
        ct = PYMPENV['CURRENT_TRACK']
        if not ct:
            self.update_information()
            return
        self.track = dict()
        self.track['PATH'] = ct.path
        self.track['artist'] = ct.artist
        self.track['title'] = ct.title
        self.track['album'] = ct.album
        self.track['year'] = ct.year
        self.track['tracknr'] = ct.trackno
        self.track['genre'] = ct.genre
        self.update_information()
        if PYMPENV['SHOW_LYRIC'] \
                and self.track['artist'] \
                and self.track['title']:
            self.fetchLyrics.emit(self.track.get('artist', QString('')),
                                  self.track.get('title', QString('')))

    def update_information(self):
        tx = self.track['PATH']
        if self.track['artist'] and self.track['title']:
            tx = '{artist}\t-\t{title}\n{album}\t({year},{tracknr}\t{genre})'.format(**self.track)
        self.customLabel.setText(tx)
