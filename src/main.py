#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from os.path import join, expanduser

sys.path.append('.')
ROOT_DIR = expanduser('~/.pymp')

if not os.path.exists(ROOT_DIR):
    os.mkdir(ROOT_DIR)
    os.mkdir(join(ROOT_DIR, 'log'))
    os.mkdir(join(ROOT_DIR, 'lyrics'))

from PyQt4 import QtGui
from pymp.pymp import PympGUI


def main_hc():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('pymp')
    PympGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_hc()
