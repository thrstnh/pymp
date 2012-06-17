from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ..lyric import LyricWorker
from ..logger import init_logger

logger = init_logger()


class LyricPanel(QWidget):
    '''
        load lyric from lyricwiki in background
    '''
    def __init__(self, parent=None):
        ''' TODO: init user interface '''
        QWidget.__init__(self, parent)
        self.artist = ''
        self.track = ''
        self.monkey = None
        self.initUI()

    def initUI(self):
        ''' init user interface '''
        self.lblTrackInfo = QLabel('')
        self.txt = QTextEdit(self)
        self.txt.setReadOnly(True)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.lblTrackInfo)
        vbox.addWidget(self.txt, 1)

    def search(self, artist, track):
        ''' search a lyrics with a thread '''
        # clear
        if self.artist == artist \
                and self.track == track:
                    logger.debug('lyrics request equals previous one! '\
                                 '{} - {}'.format(artist, track))
                    return
        else:
            logger.info('fetching lyrics: {} - {}'.format(self.artist, self.track))
        self.lblTrackInfo.setText('')
        self.txt.setText('')
        # set
        self.artist = '%s' % artist
        self.track = '%s' % track
        # search
        self.monkey = LyricWorker(self, self.artist, self.track)
        self.monkey.start()
        self.monkey.lyricFetched.connect(self.lyricChanged)

    def lyricChanged(self, lyr):
        ''' change label and textedit '''
        self.lblTrackInfo.setText('%s - %s' % (self.artist, self.track))
        self.txt.setText(lyr)

    def showEvent(self, arg1):
        ''' show user interface '''
        if self.monkey:
            self.monkey.start()
