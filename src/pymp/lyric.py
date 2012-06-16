import os
import lyricwiki
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .logger import init_logger
from .config import init_env

logger = init_logger()
PYMPENV = init_env()


class LyricWorker(QThread):
    '''
        Fetch Lyrics from LyricsWiki
    '''
    # signal called after lyrics fetched
    lyricFetched = pyqtSignal(QString)

    def __init__(self, parent, artist, title):
        QThread.__init__(self)
        self.artist = artist
        self.title = title

    def run(self):
        lyr = None
        if self.artist and self.title:
            lyr = self._read()
            if not lyr:
                try:
                    lyr = lyricwiki.get_lyrics(self.artist, self.title)
                except Exception, e:
                    logger.warning('lyrics not found or error: {}'.format(e))
                if lyr:
                    lyr = "%s - %s\n\n%s" % (self.artist, self.title, lyr)
                    self._save(lyr)
        else:
            logger.info('worker got only: {} - {}'.format(self.artist, self.title))
        if lyr:
            self.lyricFetched.emit(lyr)
            return
        else:
            logger.debug("QThread filed?...")
            self.lyricFetched.emit('no lyrics found...')
        return

    def _read(self):
        '''
            read lyrics from lyric-dir
        '''
        fp = os.path.join(PYMPENV[LYRICS_DIR], "%s-%s.txt" % (self.artist, self.title))
        try:
            with open(fp, 'r') as f:
                lyr = f.read()
            return lyr
        except Exception, e:
            logger.info("Lyrics Datei nicht gefunden: {}".format(fp))
        return ''

    def _save(self, lyr):
        '''
            save lyrics to lyric-dir for offline lyrics
        '''
        fp = os.path.join(PYMPENV['DIR_LYRICS'], "%s-%s.txt" % (self.artist, self.title))
        with open(fp, 'w') as f:
            f.write(lyr.encode('utf-8'))
