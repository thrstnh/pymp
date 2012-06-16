from PyQt4.QtGui import *
from PyQt4.QtCore import *


class BaseButton(QPushButton):

    def __init__(self, action, image, *args, **kw):
        super(BaseButton, self).__init__(*args, **kw)
        sze = QSize(24, 24)
        self.setFocusPolicy(Qt.NoFocus)
        self.clicked.connect(action)
        self.setMinimumSize(sze)
        self.setMaximumSize(sze)
        self.setIcon(QIcon(image))
        self.setStyleSheet('border: 0px solid #000000;')

class ToggleButton(BaseButton):

    def __init__(self, active, action, image_t, image_f, *args, **kw):
        super(ToggleButton, self).__init__(action, image_t, *args, **kw)
        self.status = active
        self._image_t = QIcon(image_t)
        self._image_f = QIcon(image_f)
        self.clicked.connect(self._toggle)
        self._set_icon()

    def _set_icon(self):
        if self.status:
            self.setIcon(self._image_t)
        else:
            self.setIcon(self._image_f)

    def _toggle(self):
        self.status = not self.status
        self._set_icon()
        return self.status
