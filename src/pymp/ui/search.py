import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .widgets import BaseButton
from ..logger import init_logger

logger = init_logger()


class SearchBar(QWidget):
    search = pyqtSignal(QString)
    clearSearch = pyqtSignal(QString)
    timerExpired = pyqtSignal(QString)

    def __init__(self, parent, image, timeout=300):
        QWidget.__init__(self, parent)
        self._search_timer = QTimer(self)
        self._timeout = timeout
        self._image = image
        self._clicked = 0
        self._delay = 0
        self.initUI()

    def initUI(self):
        #cssButton = "border: solid 1px black;"
        clr = BaseButton(self.clrSearch, self._image)
        #clr.setStyleSheet(cssButton)
        self._search_timer.timeout.connect(self.searchTimeout)
        self.line = QLineEdit('', self)
        self.line.textChanged.connect(self.txChanged)
        self.line.returnPressed.connect(self.txReturn)

        hbox = QHBoxLayout(self)
        hbox.addWidget(clr)
        hbox.addWidget(self.line, 1)

    def txChanged(self, t):
        self.pattern = self.line.text()
        self.search.emit(self.pattern)
        if self._search_timer.isActive():
            self._search_timer.stop()
        self._search_timer.start(self._timeout)

    def txReturn(self):
        self.search.emit(self.pattern)

    def clrSearch(self):
        self._clicked = time.time()
        logger.debug(':clrSearch')
        self.pattern = ''
        self.line.setText(self.pattern)
        self.clearSearch.emit(self.pattern)

    def searchTimeout(self):
        self._search_timer.stop()
        diff_max = self._delay + self._timeout / 1000.
        if self._clicked:
            tdiff = (time.time() - self._clicked)
            if tdiff > diff_max:
                self.timerExpired.emit(self.pattern)
                self._clicked = 0
            return
        self.timerExpired.emit(self.pattern)

    def delay(self, delay):
        self._delay = delay
