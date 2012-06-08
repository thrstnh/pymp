__author__="thrstnh"
__date__ ="$03.02.2011 15:25:25$"

from setuptools import setup,find_packages

setup (
    name = 'pymp',
    version = '0.1',
    packages=find_packages(),
    install_requires=['PyQt4',
                      'sqlite3',
                      'mutagen',
                      'lyricwiki',
                      'PyQt4.phonon'],
    author = 'thrstnh',
    author_email = 'thrstn.hllbrnd@gmail.com',
    summary = 'yet another python music player',
    url = 'https://github.com/thrstnh/pymp',
    license = 'free for all')
