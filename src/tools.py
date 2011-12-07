#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tabnanny

def tnanny(path):
    file = open(path)
    for line in file.readlines():
        print repr(line)

    # let tabnanny look at it
    tabnanny.check(path)

    
