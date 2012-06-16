import os
import os.path
import time
from os.path import expanduser
from os.path import join
from .logger import init_logger

PYMPENV = None
TABLE_PROP = None
ROOT_DIR = expanduser('~/.pymp')
TIME_PATTERN = '%Y-%m-%d--%H:%M:%S'

logger = init_logger()


def now():
    return time.strftime(TIME_PATTERN)


class PropertyDict(dict):

    _VALID_KEYS = set([])

    def __init__(self):
        super(PropertyDict, self).__init__(self)

    def __getitem__(self, key):
        if not key in self._VALID_KEYS:
            raise KeyError('"{}" not a valid key!'.format(key))
        return super(PropertyDict, self).__getitem__(key)


class PympEnv(PropertyDict):
    _VALID_KEYS = set([
            'DEBUG',
            'FILE_DB',
            'DIR_ROOT', 'DIR_LOG', 'DIR_LYRICS',
            'RANDOM', 'REPEAT', 'MUTE',
            'SHOW_LYRIC', 'SHOW_COLLECTION',
            'LFM_LOGIN', 'LFM_SCROBBLE', 'LFM_NOW_PLAYING',
            'COLLECTION_CURRENT',
            'DROP_ID',
            'ICONSET_NAME', 'ICONSET_PATH',
            'USE_SQL'])

    def __init__(self):
        super(PympEnv, self).__init__()
        self._init_defaults()

    def _init_defaults(self):
        self['DEBUG'] = False
        self['FILE_DB'] = join(ROOT_DIR, 'pymp.db')
        self['DIR_ROOT'] = ROOT_DIR
        self['DIR_LOG'] = join(ROOT_DIR, 'log')
        self['DIR_LYRICS'] = join(ROOT_DIR, 'lyrics')
        self['RANDOM'] = False
        self['REPEAT'] = False
        self['MUTE'] = False
        self['SHOW_LYRIC'] = False
        self['SHOW_COLLECTION'] = True
        self['LFM_LOGIN'] = False
        self['LFM_SCROBBLE'] = False
        self['LFM_NOW_PLAYING'] = False
        self['COLLECTION_CURRENT'] = ''
        self['DROP_ID'] = 6666666
        self['ICONSET_NAME'] = 'default'
        self['ICONSET_PATH'] = 'pymp/icons/iconsets/default/'
        self['USE_SQL'] = False

    def change_iconset(self, name, path):
        self['ICONSET_NAME'] = name
        self['ICONSET_PATH'] = path

    def _toggle(self, key):
        logger.info(':tog {} -> {}'.format(key, self[key]))
        self[key] = not self[key]

    def toggle_mute(self):
        self._toggle('MUTE')

    def toggle_lyric(self):
        self._toggle('SHOW_LYRIC')

    def toggle_collection(self):
        self._toggle('SHOW_COLLECTION')

    def _save(self):
        # TODO
        pass

    def _load(self):
        # TODO
        pass


def init_env():
    global PYMPENV
    if not PYMPENV:
        logger.info('init_env')
        PYMPENV = PympEnv()
    return PYMPENV

PYMPENV = init_env()


if not os.path.exists(ROOT_DIR):
    logger.info('create ~/.pymp files')
    os.mkdir(PYMPENV['DIR_ROOT'])
    os.mkdir(PYMPENV['DIR_LOG'])
    os.mkdir(PYMPENV['DIR_LYRICS'])


class Entry(PropertyDict):

    _VALID_KEYS = set(['SHOW', 'ROW', 'KEY', 'NAME', 'WIDTH'])

    def __init__(self, show, row, name, width):
        super(Entry, self).__init__()
        self['SHOW'] = show
        self['ROW'] = row
        self['NAME'] = name
        self['WIDTH'] = width

    @property
    def show(self):
        return self['SHOW']

    @property
    def row(self):
        return self['ROW']

    @property
    def name(self):
        return self['NAME']

    @property
    def width(self):
        return self['WIDTH']


class TableProperties(dict):

    def __init__(self):
        super(TableProperties, self).__init__()

    def set_options(self, options={}):
        # id = (SHOW, ROW, NAME, WIDTH)
        for (k,v) in options.items():
            self[k] = Entry(*v)


TABLE_OPTIONS = {
        'ID':     (True, 10, 'ID', 0),
        'HID3':   (False, 25, 'hasid3', 50),
        'TPE2':   (False, 30, 'Band', 180),
        'TPE1':   (True, 40, 'Artist', 200),
        'TIT1':   (False, 50, 'Content Group', 120),
        'TIT2':   (True, 35, 'Titel', 200),
        'TALB':   (True, 70, 'Album', 200),
        'TLEN':   (True, 80, 'Length', 60),
        'TDRC':   (True, 77, 'Year', 60),
        'TRCK':   (True, 100, 'TrackNo', 60),
        'TENC':   (False, 110, 'Encoded by', 120),
        'TFLT':   (False, 120, 'FileType', 120),
        'TDRL':   (False, 130, 'ReleaseTime', 120),
        'TLAN':   (False, 140, 'Language', 120),
        'TPUB':   (False, 150, 'Publisher', 120),
        'TCOP':   (False, 160, 'Copyright', 120),
        'TCON':   (True, 75, 'Genre', 120),
        'TCOM':   (False, 180, 'Composer', 120),
        'TSSE':   (False, 190, 'Encoding', 120),
        'TDTG':   (False, 200, 'TaggingTime', 120),
        'TBPM':   (False, 210, 'BPM', 120),
        'TPOS':   (False, 220, 'PartOfSet', 120),
        'BITR':   (False, 230, 'Bitrate', 120),
    # always hidden/last and las, just4coding
        'PATH':   (True, 999, 'PATH', 600)}


def init_table():
    global TABLE_PROP
    if not TABLE_PROP:
        logger.info('init_table')
        TABLE_PROP = TableProperties()
        TABLE_PROP.set_options(TABLE_OPTIONS)
    return TABLE_PROP

TABLE_PROP = init_table()
