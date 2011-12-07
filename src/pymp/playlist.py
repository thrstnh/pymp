#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
#from pymp.config import cfg, RANDOM, DROP_ID
#from wx.lib.pubsub import Publisher
#from pymp.mp3 import PMP3

_FILE_HEAD = '::pymp::'
_FILE_TRACKS = '::tracks::'
_FILE_QUEUE = '::queue::'
_FILE_HISTORY = '::history::'


class Playlist():
    '''
        A playlist is a part of the whole collection.
        It is like a m3u file, but there is a history and
        also a queue, which would be also saved.
        It is possible to export the playlist into the m3u format.

        Attention:
        - Only the Playlist knows, which track ist currently selected.


        Parameters:
        - tracks:
    '''
    def __init__(self, name, path, tracks={}):
        self._tracks = tracks
        # optional zum speichern
        self._path = path or ''
        self._name = name or ''
        self._queue = {}
        self._queue_order = [] # tids
        self._history = {}
        self._history_order = []
        self._current_tid = 0
        self._history_level = 0

    def next(self, keys=[]):
        raise NotImplementedError
#        self._history_reset()
#        if not self._tracks:
#            return None
#        if cfg[RANDOM]:
#            random.seed(time.time())
#            if keys:
#                self._current_tid = random.choice(keys)
#            else:
#                self._current_tid = random.choice(self._tracks.keys())
#        else:
#            if not keys:
#                keys = self._tracks.keys()
#            idx = keys.index(self._current_tid)
#            if idx < len(keys):
#                self._current_tid = keys[idx+1]
#            else:
#                self._current_tid = keys[0]
#        return {self._current_tid : self._tracks[self._current_tid]}

    @property
    def current(self):
        return {self._current_tid : self._tracks[self._current_tid]}

    @property
    def tracks(self):
        return self._tracks

    def size(self):
        return len(self._tracks)

    def clear(self):
        self._reset()

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, newpath):
        self._path = newpath

    def _reset(self):
        self._tracks = {}
        self._queue_order = []
        self._queue = {}
        self._history_order = []
        self._history = {}
        self._history_reset()

    def _handle_file(self, file):
        raise NotImplementedError
#        mp3file = PMP3(file)
#        td = []
#        if mp3file.has_id3:
#            td.append(cfg[DROP_ID]) # ID
#            td.append(mp3file.title) # TIT2
#            td.append(mp3file.artist) # TPE1
#            td.append(mp3file.album) # TALB
#            td.append(mp3file.genre) # TCON
#            td.append(mp3file.year) # TDRC
#            td.append(self._format_time(int(round(float(mp3file.length))))) # TLEN
#            td.append(mp3file.trackno) # TRCK
#            td.append(mp3file.path) # PATH
#        else:
#            h,t = os.path.split(mp3file.path)
#            td.append(cfg[DROP_ID]) # ID
#            td.append(t) # TIT2
#            td.append('') # TPE1
#            td.append('') # TALB
#            td.append('') # TCON
#            td.append('') # TDRC
#            td.append('') # TLEN
#            td.append('') # TRCK
#            td.append(mp3file.path) # PATH
#        Publisher().sendMessage('dragndrop', {cfg[DROP_ID] : td})
#        cfg[DROP_ID] += 1

    def _format_time(self, t):
        m,s = divmod(t, 60)
        if m < 60:
            return "%02i:%02i" %(m,s)
        else:
            h,m = divmod(m, 60)
            return "%i:%02i:%02i" %(h,m,s)
        
    def load(self):
        raise NotImplementedError
#        try:
#            fp = open(self._path, 'r')
#            head = fp.readline().strip()
#            assert head == _FILE_HEAD
#
#            ftracks = fp.readline().strip()
#            assert ftracks == _FILE_TRACKS
#            # tracks
#            while True:
#                line = fp.readline().strip()
#                if not line:
#                    break
#                if line == _FILE_QUEUE:
#                    break
#                if os.path.isfile(line):
#                    # drop file? faster...
#                    self._handle_file(line)
##                    t = pymp.sqldb.filter(0, line, '', [], {})
##                    self._tracks.update(t)
#            # queue
#            while True:
#                line = fp.readline().strip()
#                if not line:
#                    break
#                if line == _FILE_HISTORY:
#                    break
#                if os.path.isfile(line):
#                    # drop file? faster...
#                    self._handle_file(line)
##                    t = pymp.sqldb.filter(0, line, '', [], {})
##                    self.queue_append(t)
#            # history
#            while True:
#                line = fp.readline().strip()
#                if not line:
#                    break
#                if os.path.isfile(line):
#                    self._handle_file(line)
##                    t = pymp.sqldb.filter(0, line, '', [], {})
##                    self.history_append(t)
#
#            fp.close()
#            print "playlist.load finished!"
#            print "tracks: %d" % self.size()
#            print "queue: %d" % self.queue_size()
#            print "history: %d" % self.history_size()
#        except Exception, e:
#            print "playlist.load(%s) failed:\n%s" % (self._path, e)

    def save(self):
        raise NotImplementedError
#        try:
##            db = pymp.sqldb.filter(0, '', '', self._tracks[:], {})
#
#            print "write default playlist: %s " % self._path
#            fp = open(self._path, 'w')
#            fp.write(_FILE_HEAD)
#            fp.write('\n')
#            fp.write(_FILE_TRACKS)
#            fp.write('\n')
#            for k,v in self._tracks.items():
#                fp.write("%s" % v[8])
#                fp.write('\n')
#            fp.write(_FILE_QUEUE)
#            fp.write('\n')
#            for k in self._queue_order:
#                fp.write("%s" % self._queue[k][8])
#                fp.write('\n')
#            fp.write(_FILE_HISTORY)
#            fp.write('\n')
#            for k in self._history_order:
#                fp.write("%s" % self._history[k][8])
#                fp.write('\n')
#            fp.close()
#            print "playlist.save finished!"
#        except Exception, e:
#            print "playlist.save(%s) failed:\n%s" % (self._path, e)

    def queue_empty(self):
        if self.queue_size() > 0:
            return False
        return True

    def queue_size(self):
        return len(self._queue_order)

    def queue_append(self, items):
        [self._queue_order.append(tid) for tid in items.keys()]
        self._queue.update(items)

    def queue_get(self):
        ret = {}
        if not self.queue_empty():
            tid = self._queue_order.pop(0)
            ret = {tid : self._queue[tid]}
            if tid not in self._queue_order:
                del self._queue[tid]
        return ret

    @property
    def queue(self):
        return self._queue

    @property
    def queue_order(self):
        return self._queue_order

    @property
    def history(self):
        return self._history

    @property
    def history_order(self):
        return self._history_order

    def history_empty(self):
        if self.history_size() > 0:
            return False
        return True

    def history_size(self):
        return len(self._history_order)

    def _history_reset(self):
        self._history_level = 0

    def history_get(self):
        print "historylevel: ", self._history_level
        ret = {}
        if self._history_level >= self.history_size():
            self._history_reset()
        if not self.history_empty():
            tid = self._history_order[self._history_level]
            ret = {tid : self._history[tid]}
        self._history_level += 1
        return ret

    def history_append(self, items):
        [self._history_order.insert(0, tid) for tid in items.keys()]
        self._history.update(items)

    def append(self, track):
        self._tracks.update(track)

    def __str__(self):
        return '\n'.join(self._tracks)
