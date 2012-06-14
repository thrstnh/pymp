from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ..style import iconset


class SearchBar(QWidget):
    '''
        Control Panel for search patterns
    '''
    search = pyqtSignal(QString)
    clearSearch = pyqtSignal(QString)
    timerExpired = pyqtSignal(QString)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._search_timer = QTimer(self)
        self.initUI()

    def initUI(self):
        ''' TODO: init user interface '''
        #pref = '../data/'
        #cssButton = "border-style: flat; border-width: 0px; border-color: black;"
        clr = QPushButton(QIcon(iconset['cancel']), "", self)
        clr.setFocusPolicy(Qt.NoFocus)
        clr.clicked.connect(self.clrSearch)
        clr.setMinimumSize(QSize(16,16))
        clr.setMaximumSize(QSize(16,16))
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

        '''
            start a double click timer for 300ms.
            if dclick: fill playlist with node-children
            if singleclick: open tree node
        '''
        if self._search_timer.isActive():
            self._search_timer.stop()
        self._search_timer.start(1000)

    def txReturn(self):
        self.search.emit(self.pattern)
        #self.pattern = self.line.text()
        #self.search.emit(self.pattern)

    def clrSearch(self):
        ''' clear search '''
        self.pattern = ''
        self.line.setText(self.pattern)
        self.clearSearch.emit(self.pattern)

    def searchTimeout(self):
        self._search_timer.stop()
        self.timerExpired.emit(self.pattern)
