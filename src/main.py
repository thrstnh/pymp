#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from pymp.pymp import PympGUI

sys.path.append('.')

def main_hc():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('pymp')
    pympgui = PympGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_hc()
