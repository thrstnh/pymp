from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ..mp3 import PMP3
from ..logger import init_logger
from ..style import iconset

logger = init_logger()


class ID3Edit(QDialog):
    '''
        ID3 Tag Editor
    '''
    def __init__(self, parent=None, fp=None):
        QDialog.__init__(self, parent)
        self.fp = fp
        self.data = self.load(self.fp)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        for (k,v) in self.data.items():
            hbox = QHBoxLayout(self)
            lbl = QLabel(str(k), self)
            line = QLineEdit(str(v), self)
            hbox.addWidget(lbl)
            hbox.addWidget(line, 1)
            vbox.addLayout(hbox)

        hbox = QHBoxLayout(self)
        ok = QPushButton(QIcon(iconset['ok']), "", self)
        ok.clicked.connect(self.onOk)
        cancel = QPushButton(QIcon(iconset['cancel']), "", self)
        cancel.clicked.connect(self.onCancel)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        vbox.addLayout(hbox)

        #self.setLayout(vbox)
        self.setWindowTitle('ID3 Editor')
        self.resize(300, 800)

    def load(self, fp):
        '''
            load mp3 id3 meta data from file as dict
        '''
        return PMP3(fp).all()

    def onOk(self):
        ''' exit dialog with ok'''
        logger.info("ok")
        self.close()

    def onCancel(self):
        ''' exit dialog with cancel '''
        logger.info("cancel")
        self.close()
