#!/usr/bin/env python
from setuptools import setup, find_packages

requires = ['mutagen', 'lyricwiki']

setup(name = 'pymp',
      version = '0.1',
      author = 'thrstnh',
      author_email = 'thrstn.hllbrnd@gmail.com',
      url = 'https://github.com/thrstnh/pymp',
      packages=find_packages(),
      install_requires=requires,
      license = 'free for all')
