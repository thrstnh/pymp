from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ..mp3 import PMP3


class TrackInfoBar(QWidget):
    '''
        Track Information Panel with current track
    '''
    # fetch lyrics with new track information to keep the right chain
    fetchLyrics = pyqtSignal(QString, QString)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()
        self.track = dict()
        self.track['artist'] = ''
        self.track['title'] = ''
        self.track['album'] = ''
        self.track['year'] = ''
        self.track['tracknr'] = ''
        self.track['genre'] = ''

    def initUI(self):
        ''' TODO: init user interface '''
        self.customLabel = QLabel(self)
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.customLabel)
        vbox.addLayout(hbox)

    def update(self, qstr):
        '''
            fill fields with data
        '''
        mpfile = PMP3(qstr)
        self.track['artist'] = mpfile.artist
        self.track['title'] = mpfile.title
        self.track['album'] = mpfile.album
        self.track['year'] = mpfile.year
        self.track['tracknr'] = mpfile.trackno
        self.track['genre'] = mpfile.genre
        self.updateInformation()
        self.fetchLyrics.emit(self.track.get('artist', ''),
                              self.track.get('title', ''))

    def updateInformation(self):
        ''' sync vars with gui-labels '''
        tx = '{artist}\t-\t{title}\n{album}\t({year},{tracknr}\t{genre})'.format(**self.track)
        self.customLabel.setText(tx)