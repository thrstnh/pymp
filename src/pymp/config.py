import sys
import os
import os.path
import copy
import json
from os.path import expanduser
from os.path import join
from .logger import init_logger


ENCODING = sys.stdout.encoding or sys.getfilesystemencoding()
PYMPENV = None
TABLE_PROP = None
ROOT_DIR = expanduser('~/.pymp')
FILE_CONFIG = join(ROOT_DIR, 'config')
TIME_PATTERN = '%Y-%m-%d--%H:%M:%S'

logger = init_logger()
logger.debug(':HOME {}'.format(ROOT_DIR))
logger.debug(':encoding {}'.format(ENCODING))


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
            'DEBUG', 'APP', 'VERSION',
            'FILE_DB',
            'DIR_ROOT', 'DIR_LOG', 'DIR_LYRICS',
            'RANDOM', 'REPEAT', 'MUTE',
            'SHOW_LYRIC', 'SHOW_COLLECTION',
            'LFM_LOGIN', 'LFM_SCROBBLE', 'LFM_NOW_PLAYING',
            'COLLECTION_CURRENT',
            'CURRENT_TRACK', 'CURRENT_DMP3', 'LAST_TRACK',
            'DROP_ID',
            'ICONSET',
            'USE_SQL', 'FAST_CLIENT', 'AUTO_FOCUS',
            'SEARCH_TIMEOUT',
            'TAG_UPDATE'])

    def __init__(self):
        super(PympEnv, self).__init__()
        try:
            self.load()
        except:
            self._init_defaults()

    def _init_defaults(self):
        self['DEBUG'] = False
        self['APP'] = 'pymp'
        self['VERSION'] = '0.1'
        self['FILE_DB'] = join(ROOT_DIR, 'pymp.db')
        self['DIR_ROOT'] = ROOT_DIR
        self['DIR_LOG'] = join(ROOT_DIR, 'log')
        self['DIR_LYRICS'] = join(ROOT_DIR, 'lyrics')
        self['RANDOM'] = True
        self['REPEAT'] = False
        self['MUTE'] = False
        self['SHOW_LYRIC'] = True
        self['SHOW_COLLECTION'] = True
        self['LFM_LOGIN'] = False
        self['LFM_SCROBBLE'] = False
        self['LFM_NOW_PLAYING'] = False
        self['COLLECTION_CURRENT'] = ''
        self['CURRENT_TRACK'] = None
        self['CURRENT_DMP3'] = None
        self['LAST_TRACK'] = None
        self['DROP_ID'] = 6666666
        self['ICONSET'] = {'default': 'pymp/icons/iconsets/default/'}
        self['USE_SQL'] = False
        self['FAST_CLIENT'] = True
        # focus track on next play
        self['AUTO_FOCUS'] = True
        self['SEARCH_TIMEOUT'] = 500
        # this is an option for collection rescan,
        # if it is True, the rescan of a collection
        # also checks for new or updated id3-tags,
        # otherwise only for new file in the collection.
        self['TAG_UPDATE'] = False
        # do not exit; minimize
        self['CLOSE_ON_HIDE'] = False

    def change_iconset(self, name, path):
        self['ICONSET_NAME'] = name
        self['ICONSET_PATH'] = path

    def toggle(self, key):
        self[key] = not self[key]
        self.save()
        logger.info(':tog  {} -> {}'.format(key, self[key]))

    def toggle_mute(self):
        self.toggle('MUTE')

    def toggle_lyric(self):
        self.toggle('SHOW_LYRIC')

    def toggle_collection(self):
        self.toggle('SHOW_COLLECTION')

    def save(self):
        me = copy.deepcopy(self)
        if me['CURRENT_TRACK']:
            del me['CURRENT_TRACK']
        with open(FILE_CONFIG, 'w') as fp:
            fp.write(json.dumps(me, sort_keys=True, indent=4))

    def load(self):
        try:
            self.update(self._load_config())
            self['CURRENT_TRACK'] = None
        except:
            self._init_defaults()

    def _load_config(self):
        with open(FILE_CONFIG) as fp:
            return json.loads(fp.read())

    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=4)


def init_env():
    global PYMPENV
    if not PYMPENV:
        PYMPENV = PympEnv()
    return PYMPENV

PYMPENV = init_env()
logger.debug(':env\n{}'.format('\n'.join(
                ['    {:20} -> {}'.format(k, v)
                    for k,v in PYMPENV.items()])))


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
