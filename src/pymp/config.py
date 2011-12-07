#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
from os.path import expanduser
from os.path import join
import time

#print "OS: ", os.uname()

#TODO
#PyEmbeddedImage
# change this!
ROOT_DIR    = expanduser('~/.pymp')

DEBUG       =   'DEBUG'
PYMP_DIR    =   'PYMP_DIR'
DB_FILE     =   'DBFILE'
LOG_DIR     =   'LOGDIR'
LYRICS_DIR  =   'LYRICSDIR'
COLLECTIONS =   'COLLECTIONS'
CLK_SEARCH  =   'CLK_SEARCH'
RANDOM      =   'RANDOM'
REPEAT      =   'REPEAT'
SHOW_LYRIC  =   'SHOW_LYRIC'
SHOW_TREE   =   'SHOW_TREE'
DB_FILE_TEST =  'DB_FILE_TEST'
LFM_LOGIN =  'LFM_LOGIN'
LFM_SCROBBLE =  'LFM_SCROBBLE'
LFM_NOW_PLAYING = 'LFM_NOW_PLAYING'
CURRENT_COLLECTION = 'CURRENT_COLLECTION'
DEFAULT_COLLECTION = 'DEFAULT_COLLECTION'
DEFAULT_PLAYLIST = 'DEFAULT_PLAYLIST'
DROP_ID         = 'DROP_ID'

cfg = {
    DEBUG       : False,
    PYMP_DIR    : ROOT_DIR,
    DB_FILE     : join(ROOT_DIR, 'pymp.db'),
    LOG_DIR     : join(ROOT_DIR, 'log'),
    LYRICS_DIR  : join(ROOT_DIR, 'lyrics'),
    DEFAULT_PLAYLIST : join(ROOT_DIR, 'playlist.pym'),
    CLK_SEARCH  : 0.5,
    RANDOM    : True,
    REPEAT    : True,
    SHOW_LYRIC  : True,
    SHOW_TREE   : True,
    DROP_ID     : 6666666,
    LFM_LOGIN   : True,
    LFM_SCROBBLE: False,
    LFM_NOW_PLAYING: False,
    CURRENT_COLLECTION : None,
}

if not os.path.exists(ROOT_DIR):
    os.mkdir(ROOT_DIR)
    os.mkdir(cfg[LOG_DIR])
    os.mkdir(cfg[LYRICS_DIR])

TBL_ID      =   'ID'
TBL_HID3    =   'HID3'
TBL_PATH    =   'PATH'
TBL_TPE2    =   'TPE2'
TBL_TPE1    =   'TPE1'
TBL_TIT1    =   'TIT1'
TBL_TIT2    =   'TIT2'
TBL_TALB    =   'TALB'
TBL_TLEN    =   'TLEN'
TBL_TDRC    =   'TDRC'
TBL_TRCK    =   'TRCK'
TBL_TENC    =   'TENC'
TBL_TFLT    =   'TFLT'
TBL_TDRL    =   'TDRL'
TBL_TLAN    =   'TLAN'
TBL_TPUB    =   'TPUB'
TBL_TCOP    =   'TCOP'
TBL_TCON    =   'TCON'
TBL_TCOM    =   'TCOM'
TBL_TSSE    =   'TSSE'
TBL_TDTG    =   'TDTG'
TBL_TBPM    =   'TBPM'
TBL_TPOS    =   'TPOS'
TBL_BITR    =   'BITR'

# show | order | name | width
tbl = {
    0 : (),
    1 : (),
    }

tbl = {
    TBL_ID    :   (True, 10, 'ID', 0),
    TBL_HID3  :   (False, 25, 'hasid3', 50),
    TBL_TPE2  :   (False, 30, 'Band', 180),
    TBL_TPE1  :   (True, 40, 'Artist', 200),
    TBL_TIT1  :   (False, 50, 'Content Group', 120),
    TBL_TIT2  :   (True, 35, 'Titel', 200),
    TBL_TALB  :   (True, 70, 'Album', 200),
    TBL_TLEN  :   (True, 80, 'Length', 60),
    TBL_TDRC  :   (True, 77, 'Year', 60),
    TBL_TRCK  :   (True, 100, 'TrackNo', 60),
    TBL_TENC  :   (False, 110, 'Encoded by', 120),
    TBL_TFLT  :   (False, 120, 'FileType', 120),
    TBL_TDRL  :   (False, 130, 'ReleaseTime', 120),
    TBL_TLAN  :   (False, 140, 'Language', 120),
    TBL_TPUB  :   (False, 150, 'Publisher', 120),
    TBL_TCOP  :   (False, 160, 'Copyright', 120),
    TBL_TCON  :   (True, 75, 'Genre', 120),
    TBL_TCOM  :   (False, 180, 'Composer', 120),
    TBL_TSSE  :   (False, 190, 'Encoding', 120),
    TBL_TDTG  :   (False, 200, 'TaggingTime', 120),
    TBL_TBPM  :   (False, 210, 'BPM', 120),
    TBL_TPOS  :   (False, 220, 'PartOfSet', 120),
    TBL_BITR  :   (False, 230, 'Bitrate', 120),
    # always hidden/last and las, just4coding
    TBL_PATH  :   (True, 999, 'PATH', 600),
}


IMG_STOP        = 'IMG_STOP'
IMG_PLAY        = 'IMG_PLAY'
IMG_PAUSE       = 'IMG_PAUSE'
IMG_PREV        = 'IMG_PREV'
IMG_NEXT        = 'IMG_NEXT'
IMG_REPEAT_T    = 'IMG_REPEAT_T'
IMG_REPEAT_F    = 'IMG_REPEAT_F'
IMG_RANDOM_T    = 'IMG_RANDOM_T'
IMG_RANDOM_F    = 'IMG_RANDOM_F'
IMG_MUTE_T        = 'IMG_MUTE_T'
IMG_MUTE_F        = 'IMG_MUTE_F'
IMG_CLEAR       = 'IMG_MUTE'
IMG_PYMP        = 'IMG_PYMP'
IMG_LOVE_TRACK  = 'IMG_LOVE_TRACK'
IMG_REFRESH     = 'IMG_REFRESH'
IMG_LASTFM_T    = 'IMG_LASTFM_T'
IMG_LASTFM_F    = 'IMG_LASTFM_F'
IMG_TREE_T      = 'IMG_TREE_T'
IMG_TREE_F      = 'IMG_TREE_F'
IMG_LYRIC_T     = 'IMG_LYRIC_T'
IMG_LYRIC_F     = 'IMG_LYRIC_F'
IMG_OPEN        = 'IMG_OPEN'
IMG_SAVE        = 'IMG_SAVE'
IMG_SHUFFLE     = 'IMG_SHUFFLE'
IMG_NEW         = 'IMG_NEW'
IMG_DELETE      = 'IMG_DELETE'
IMG_CANCEL      = 'IMG_CANCEL'
IMG_OK          = 'IMG_OK'
IMG_SETTINGS    = 'IMG_SETTINGS'
IMG_CUT         = 'IMG_CUT'
IMG_EXIT        = 'IMG_EXIT'
IMG_FILTER      = 'IMG_FILTER'
IMG_SEARCH      = 'IMG_SEARCH'
IMG_FOCUS_TRACK = 'IMG_FOCUS_TRACK'
IMG_WARNING     = 'IMG_WARNING'
IMG_ERROR       = 'IMG_ERROR'
IMG_ARR_UP      = 'IMG_ARR_UP'
IMG_ARR_DOWN      = 'IMG_ARR_DOWN'
IMG_ARR_LEFT      = 'IMG_ARR_LEFT'
IMG_ARR_RIGHT      = 'IMG_ARR_RIGHT'

icon_set = {
    # toggle PLAY / PAUSE
    IMG_PLAY        : 'playback_play.png',
    IMG_PAUSE       : 'playback_pause.png',
    # toggle repeat 0 / 1
    IMG_REPEAT_T    : 'repeat_t.png',
    IMG_REPEAT_F    : 'repeat_f.png',
    # toggle random 0 / 1
    IMG_RANDOM_T    : 'random_t.png',
    IMG_RANDOM_F    : 'random_f.png',
    # toggle mute 0 / 1
    IMG_MUTE_T        : 'speaker.png',
    IMG_MUTE_F        : 'speaker.png',
    # toggle lfm 0 / 1
    IMG_LASTFM_T    : 'lfm_t.png',
    IMG_LASTFM_F    : 'lfm_f.png',
    # toggle tree 0 / 1
    IMG_TREE_T	: 'layout_lp.png',
    IMG_TREE_F	: 'layout_lm.png',
    # toggle lyric 0 / 1
    IMG_LYRIC_T	: 'layout_rp.png',
    IMG_LYRIC_F	: 'layout_rm.png',
    # single icons
    IMG_PYMP        : 'pymp.png',
    IMG_OPEN	: 'open.png',
    IMG_SAVE	: 'save.png',
    IMG_SHUFFLE	: 'shuffle.png', # dice
    IMG_NEW		: 'new.png', # example playlist
    IMG_DELETE	: 'delete.png',
    IMG_STOP        : 'playback_stop.png',
    IMG_PREV        : 'playback_prev.png',
    IMG_NEXT        : 'playback_next.png',
    IMG_CLEAR       : 'clear.png',
    IMG_CANCEL	: 'cancel.png',
    IMG_OK		: 'ok.png',
    IMG_SETTINGS	: 'settings.png',
    IMG_CUT		: 'cut.png',
    IMG_EXIT	: 'exit.png',
    IMG_REFRESH     : 'refresh.png',
    IMG_FILTER	: 'filter.png',
    IMG_SEARCH	: 'search.png',
    IMG_LOVE_TRACK  : 'love_track.png',
    IMG_FOCUS_TRACK : 'focus.png',
    IMG_WARNING	: 'warning.png',
    IMG_ERROR	: 'error.png',
    IMG_ARR_UP	: 'arr_up.png',
    IMG_ARR_DOWN	: 'arr_down.png',
    IMG_ARR_LEFT	: 'arr_left.png',
    IMG_ARR_RIGHT	: 'arr_right.png',
}

def init_icon_set(path):
    global icon_set
    path = 'data/iconsets/default'
#    print "%s" % path
    for key, v in icon_set.items():
        icon_set[key] = join(path, v)
#        print key, icon_set[key]
    return icon_set

TIME_PATTERN = '%Y-%m-%d--%H:%M:%S'
def now():
    return time.strftime(TIME_PATTERN)

# events
PYMP_EVENT_NEXT = 'PYMP_EVENT_NEXT'
PYMP_EVENT_CURRENT = 'PYMP_EVENT_CURRENT'
PYMP_EVENT_DRAGNDROP = 'PYMP_EVENT_DRAGNDROP'
PYMP_EVENT_COLLECTION_SCANNED = 'PYMP_EVENT_COLLECTION_SCANNED'