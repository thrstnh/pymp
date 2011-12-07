#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pymp.config import cfg, LOG_DIR, DB_FILE
from pymp.mp3 import PMP3
import pymp.sqldb
import time
import threading
import sqlite3
from multiprocessing import Process, Pipe

__all__ = ["Collections"]


class Collections():
    '''
        Collections ist the top class for every collection.
    '''
    def __init__(self):
        self.reload()

    def reload(self):
        self._collections = {}
        self._collection_db = pymp.sqldb.get_collections()
        for k,v in self._collection_db.items():
            self.add(v['name'], v['path'])
    
    def get_collections(self):
        return self._collection_db

    def get(self, name):
        return self._collections.get(name)

    def names(self):
        return self._collections.keys()

    def add(self, name, path):
        self._collections.update({name : Collection(name, path)})

    def __getitem__(self, no):
        if no in self._collections:
            return self._collections[no]
        else:
            return None

    def __str__(self):
        return 'Collections:\n %s' % self._collections


class Collection():
    '''
        A Collection contains the name and path to the collection.
        It scans the path or reads the tracks from the sql database.
        A subset of the collection can be given to a playlist, which
        controls the play behaviour.

        example execution:
        >>> from pymp import Collection
        >>> cp = '/home/matflasch/musik'

        >>> c = Collection('test', cp)
        >>> print "scan entire collection..."
        >>> c.rescan()
        >>> print "done."
    '''
    def __init__(self, name, path):
        self._cpath = path
        self._name = name
        # id from db
        self._init_cid()
        self._load()
        # fs data
        self._files = []
        self._files_not_accepted = []
        # fs rescan count
        self._count = 0
        self._count_exists = 0
        self._count_new = 0
        # collection worker
        self._cw = None
        
    def _init_cid(self):
        self._cid = pymp.sqldb.get_collection_id(self._name)

    @property
    def cid(self):
        return self._cid
    
    @property
    def name(self):
        return self._name
    
    @cid.setter
    def cid(self, cid):
        raise Exception('cid...')

    @property
    def data_full(self):
        return pymp.sqldb.filter(self.cid, u'',u'', [], {})

    def reload(self):
        self._load()
        return True

    def _load(self):
        self._data = {}
        return True

    def size(self):
        return -1

    def getName(self):
        return self._name

    def get_data(self):
        return self._data

    def rescan(self):
        if self._cw:
            if self._cw.is_alive():
                return False
        else:
            self._cw = CollectionWorkerThread(self._cid, self._name, self._cpath)
            return True

    @property
    def scanning(self):
        if self._cw:
            return self._cw.is_alive()
        return False

    def is_scanning(self):
        if self._cw:
            return self._cw.is_alive()
        return False

    def stop_scan(self):
        if not self._cw:
            return True
        if self._cw.is_alive():
            self._cw.running = False
            self._cw.join()
            del self._cw
            self._cw = None
            return True

    def __str__(self):
        return 'Collection: %s (%s)' % (self._name, self.size())


class CollectionWorkerThread(threading.Thread):
    def __init__(self, cid, name, path):
        threading.Thread.__init__(self)
        self.running = True
        self.cid = cid
        self.path = path
        self._conn, child_conn = Pipe()
        self._proc = Process(target=CollectionWorkerProcess, args=(cid, name, path, child_conn))
        self.start()

    def run(self):
        self._proc.start()
        while self.running:
            data = self._conn.recv()
            if 'FINISHED' in data:
                fi, da = data.split('::::')
                self.running = False
                continue
            elif 'STATUS' in data:
                print data.encode('utf-8')
                st, da = data.split('::::')
                alb, cnt, cnt_new, cnt_exi, cnt_not_acc, tstart, tstatus = da.split('::')
            elif data.find(':') > 0:
                pass
                
        attempt = 0
        while self._proc.is_alive() and attempt < 10:
            self._proc.terminate()
            attempt += 1
            time.sleep(0.2)


class CollectionWorkerProcess(object):
    def __init__(self, cid, name, path, conn):
        self._cid = cid
        self._name = name
        self._path = path
        self._conn_pipe = conn
        self._files = []
        self._files_not_accepted = []
        # fs rescan count
        self._count = 0
        self._count_exists = 0
        self._count_new = 0
        self._files_to_scan = 0
        self.start()

    def start(self):
        self._start_time = time.time()
        self.conn = sqlite3.connect(cfg[DB_FILE])
        self.sqlc = self.conn.cursor()
        self.rescan()
        self.conn.close()

    def rescan(self):
        try:
#            self._conn_pipe.send('count files...')
#            os.path.walk(self._path, self.__count, None)
#            self._conn_pipe.send('%s files accepted' % self._files_to_scan)
            self._count = 0
            self._count_exists = 0
            self._count_new = 0
            try:
                os.path.walk(self._path, self.__scan, None)
            except Exception, e:
                print "os.path.walk failed!"
            self._stop_time = time.time()
            self._conn_pipe.send(u'FINISHED::::%s::%d::%d::%d::%d::%s::%s' % (self._name,
                            self._count or 0,
                            self._count_exists or 0,
                            self._count_new or 0,
                            len(self._files_not_accepted) or 0,
                            self._start_time,
                            self._stop_time))

            print "done."
        except Exception, e:
            print "rescan failed!", e
            
    def get_track_id(self, cid, path):
        trackid = 0
        try:
            sql = u'SELECT id FROM track WHERE path = ? and collection_id = ?;'
            params = (path, cid)
            self.sqlc.execute(sql, params)
            item = self.sqlc.fetchone()
            trackid = item[0]
            return trackid
        except TypeError:
            pass
        except Exception, e:
            print "get_track_id::1\n%s\n%s\n%s\n\n" % (sql, params, e)
        return trackid

    def now(self, ):
        return int(time.time())
    
    def get_artist_id(self, cid=0, tpe1='', tpe2=''):
        artid = 0
        if cid:
            try:
                sql = u'SELECT id FROM artist WHERE tpe1 = ? AND collection_id = ?;'
                params = (tpe1, cid)
                self.sqlc.execute(sql, params)
                item = self.sqlc.fetchone()
                artid = item[0]
                return artid
            except TypeError:
                pass
            except Exception, e:
                print "get_artist_id::1\n%s\n%s\n%s\n\n" % (sql, params, e)

            try:
                sql = u'INSERT INTO artist (collection_id, tpe1, dateadd, datechg) \
                                VALUES (?, ?, ?, ?);'
                params = (cid, tpe1, self.now(), self.now())
                self.sqlc.execute(sql, params)
                self.conn.commit()
            except Exception, e:
                print "get_artist_id::2\n%s\n%s\n%s\n\n" % (sql, params, e)

            try:
                sql = u'SELECT id FROM artist WHERE tpe1 = ? \
                            AND collection_id = ?;'
                params = (tpe1, cid)
                self.sqlc.execute(sql, params)
                item = self.sqlc.fetchone()
                artid = item[0]
                return artid
            except Exception, e:
                print "get_artist_id::3\n%s\n%s\n%s\n\n" % (sql, params, e)
        return artid
    
    def get_album_id(self, cid=0, talb='', tpos='', tdrc=''):
        albid = 0
        if cid:
            try:
                sql = u'''SELECT id FROM album WHERE talb = ?
                        AND collection_id = ?; '''
                params = (talb, cid)
                self.sqlc.execute(sql, params)
                item = self.sqlc.fetchone()
                albid = item[0]
                return albid
            except TypeError:
                pass
            except Exception, e:
                print "get_album_id::1\n%s\n%s\n%s\n\n" % (sql, params, e)
                pass

            try:
                sql = u''' INSERT INTO album (collection_id, talb, tpos, tdrc, dateadd, datechg)
                                    VALUES (?, ?, ?, ?, ?, ?); '''
                params = (cid, talb, tpos, tdrc, self.now(), self.now())
                self.sqlc.execute(sql, params)
                self.conn.commit()
            except Exception, e:
                print "get_album_id::2\n%s\n%s\n%s\n\n" % (sql, params, e)

            try:
                sql = u'''SELECT id FROM album WHERE talb = ?; '''
                params = talb,
                self.sqlc.execute(sql, params)
                item = self.sqlc.fetchone()
                albid = item[0]
                return albid
            except Exception, e:
                print "get_album_id::3\n%s\n%s\n%s\n\n" % (sql, params, e)
        return albid

    def get_genre_id(self, genre=''):
        genid = 0
        try:
            sql = u'''SELECT id FROM genre WHERE tcon = ?; '''
            params = genre,
            self.sqlc.execute(sql, params)
            item = self.sqlc.fetchone()
            genid = item[0]
            return genid
        except TypeError:
            pass
        except Exception, e:
            print "get_genre_id::1\n%s\n%s\n%s\n\n" % (sql, params, e)

        try:
            sql = u''' INSERT INTO genre (tcon, dateadd)
                            VALUES (?, ?); '''
            params = (genre, self.now())
            self.sqlc.execute(sql, params)
            self.conn.commit()
        except Exception, e:
            print "get_genre_id::2\n%s\n%s\n%s\n\n" % (sql, params, e)

        try:
            sql = u'''SELECT id FROM genre WHERE tcon = ?; '''
            params = genre,
            self.sqlc.execute(sql, params)
            item = self.sqlc.fetchone()
            genid = item[0]
            return genid
        except Exception, e:
            print "get_genre_id::3\n%s\n%s\n%s\n\n" % (sql, params, e)
        return genid

    def get_addinfo_id(self, k, v):
        addid = 0
        try:
            sql = u'''SELECT id FROM addinfo WHERE name = ?
                    AND value = ?; '''
            params = (k,v)
            self.sqlc.execute(sql, params)
            item = self.sqlc.fetchone()
            addid = item[0]
            return addid
        except TypeError:
            pass
        except Exception, e:
            print "get_addinfo_id::1\n%s\n%s\n%s\n\n" % (sql, params, e)

        try:
            sql = u''' INSERT INTO addinfo (name, value, dateadd)
                VALUES (?, ?, ?); '''
            params = (k, v, self.now())
            self.sqlc.execute(sql, params)
            self.conn.commit()
        except Exception, e:
            print "get_addinfo_id::2\n%s\n%s\n%s\n\n" % (sql, params, e)

        try:
            sql = u'''SELECT id FROM addinfo WHERE name = ?
                    AND value = ?; '''
            params = (k,v)
            self.sqlc.execute(sql, params)
            item = self.sqlc.fetchone()
            addid = item[0]
            return addid
        except Exception, e:
            print "get_addinfo_id::3\n%s\n%s\n%s\n\n" % (sql, params, e)
        return addid

    def connect_sat_addinfo(self, trackid, addinfoid):
        try:
            sql = u''' INSERT INTO sat_addinfo (track_id, addinfo_id, dateadd)
                VALUES (?, ?, ?); '''
            params = (trackid, addinfoid, self.now())
            self.sqlc.execute(sql, params)
            self.conn.commit()
        except Exception, e:
            print "connect_sat_addinfo::\n%s\n%s\n%s\n\n" % (sql, params, e)

    def insert(self, cid, path, kwargs):
        try:
            sql = u' SELECT * FROM track WHERE collection_id = ? AND path = ?; '
            params = (cid, path)
            self.sqlc.execute(sql, params)
            item = self.sqlc.fetchone()
            if item[0]:
                return item
        except TypeError:
            pass
        except Exception, e:
            print "connect_sat_addinfo::0\n%s\n%s\n%s\n\n" % (sql, params, e)

        hid3 = 0
        # without id3
        if not kwargs:
            try:
                sql = u'INSERT INTO track (collection_id, tit2, path, hid3, artist_id, album_id, genre_id, \
                                length, bitrate, trck, playcount, playlast, dateadd, datechg) VALUES \
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
                params = (cid, '', path, hid3, 0, 0, 0,
                            0, 0, '', 0, 0, self.now(), self.now())
                self.sqlc.execute(sql, params)
                self.conn.commit()
                trackid = self.sqlc.lastrowid
            except Exception, e:
                print "insert::1\n%s\n%s\n%s\n\n" % (sql, params, e)

        # with id3
        if kwargs:
            hid3 = 1
            # check: artist exists?
            artid = 0
            if 'TPE1' in kwargs:
                tpe1 = u"%s" % kwargs['TPE1']
                tpe2 = u''
                if 'TPE2' in kwargs:
                    tpe2 = u"%s" % kwargs['TPE2']
                    del kwargs['TPE2']
                artid = self.get_artist_id(cid, tpe1, tpe2)
                del kwargs['TPE1']

            # album
            albid = 0
            if 'TALB' in kwargs:
                talb = u"%s" % (kwargs['TALB'])
                tpos = u''
                tdrc = u''
                if 'TPOS' in kwargs:
                    tpos = u"%s" % (kwargs['TPOS'])
                    del kwargs['TPOS']
                if 'TDRC' in kwargs:
                    tdrc = u"%s" % (kwargs['TDRC'])
                    del kwargs['TDRC']
                albid = self.get_album_id(cid, talb, tpos, tdrc)
                del kwargs['TALB']

            # genre
            genid = 0
            if 'TCON' in kwargs:
                tcon = u"%s" % (kwargs['TCON'])
                genid = self.get_genre_id(tcon)
                del kwargs['TCON']

            # title
            title = ''
            if 'TIT2' in kwargs:
                title = u"%s" % (kwargs['TIT2'])
                del kwargs['TIT2']

            # length
            length = 0
            if 'TLEN' in kwargs:
                length = int(float(kwargs['TLEN']) or 0.0) or 0
                del kwargs['TLEN']

            # bitrate
            bitrate = 0
            if 'BITR' in kwargs:
                bitrate = kwargs['BITR'] or 0
                del kwargs['BITR']

            # trackno
            trck = ''
            if 'TRCK' in kwargs:
                trck = u"%s" % (kwargs['TRCK'])
                del kwargs['TRCK']

            playcount = 0
            playlast = 0

            trackid = 0
            try:
                sql = u'INSERT INTO track (collection_id, tit2, path, hid3, artist_id, album_id, genre_id, \
                                length, bitrate, trck, playcount, playlast, dateadd, datechg) VALUES \
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
                params = (cid, title, path, hid3, artid, albid, genid,
                            length, bitrate, trck, playcount, playlast, self.now(), self.now())
                self.sqlc.execute(sql, params)
                self.conn.commit()
                trackid = self.sqlc.lastrowid
            except Exception, e:
                print "insert::2\n%s\n%s\n%s\n\n" % (sql, params, e)

            try:
                sql = u' SELECT * FROM track WHERE collection_id = ? AND path = ?;'
                params = (cid, path)
                self.sqlc.execute(sql, params)
                item = self.sqlc.fetchone()
                if len(kwargs) > 0:
                    for k,v in kwargs.items():
                        k = u"%s" % k
                        v = u"%s" % v
                        addid = self.get_addinfo_id(k, v)
                        self.connect_sat_addinfo(trackid, addid)
                return item
            except Exception, e:
                print "insert::3\n%s\n%s\n%s\n\n" % (sql, params, e)
        return False

    def __scan(self, dummy, dirname, filesindir):
        for fname in filesindir:
            file = None
            try:
                file = os.path.join(dirname, fname)
                mp3file = None
                data = None
                if self._accept(file):
                    self._count += 1
                    self._files.append(file)
                    data = self.get_track(self._cid, file)
                    if not data:
                        self._count_new += 1
                        mp3file = PMP3(file)
                        if mp3file:
                            if not mp3file.has_id3:
                                self.insert(int(self._cid), file, {})
                            else:
                                mp3all = mp3file.all()
                                if mp3all:
                                    self.insert(int(self._cid), file, mp3all)
                    else:
                        self._count_exists += 1
                        
                    if self._count % 10 == 0 or self._count < 10:
                        self._conn_pipe.send(u"%s:%s" % (self._name, self._count))
                        self._status_time = time.time()
                        self._conn_pipe.send(u'STATUS::::%s::%d::%d::%d::%d::%s::%s' % (self._name,
                                    self._count or 0,
                                    self._count_exists or 0,
                                    self._count_new or 0,
                                    len(self._files_not_accepted) or 0,
                                    self._start_time,
                                    self._status_time))
            except Exception, e:
                if file:
                    print "__scan::error: ", file, e
                else:
                    print "__scan::error", e

    def __count(self, arg, dirname, filesindir):
        for fname in filesindir:
            file = os.path.join(dirname, fname)
            if self._accept(file):
                self._files_to_scan += 1
                
    def _accept(self, path):
        root, ext = os.path.splitext(path)
        try:
            path.encode('utf-8')
        except UnicodeError, e:
            print "_accept:err:encode", type(path)
            return False

        if ext in ('.mp3', '.MP3', '.Mp3', '.mP3'):
            return True
        self._files_not_accepted.append(path)
        return False

    def get_track(self, cid, path):
        sql = u'''SELECT
                        artist.tpe1,
                        album.talb,
                        track.tit2,
                        track.id,
                        track.trck,
                        album.tdrc,
                        genre.tcon,
                        track.path,
                        track.length,
                        track.hid3
                    FROM track
                        LEFT JOIN artist
                            ON track.artist_id = artist.id
                        LEFT JOIN album
                            ON track.album_id = album.id
                        LEFT JOIN genre
                            ON track.genre_id = genre.id
                    WHERE track.collection_id = ?
                        AND path = ? '''
        #print sql
        try:
            params = (cid, path)
            self.sqlc.execute(sql, params)
            ret = []
            for row in self.sqlc:
                retval = {}
                if row[0]:
                    retval['tpe1'] = row[0]
                else:
                    retval['tpe1'] = u''
                if row[1]:
                    retval['talb'] = row[1]
                else:
                    retval['talb'] = u''
                if row[2]:
                    retval['tit2'] = row[2]
                else:
                    retval['tit2'] = u''
                if row[3]:
                    retval['tid'] = row[3]
                else:
                    retval['tid'] = u''
                if row[4]:
                    retval['trck'] = row[4]
                else:
                    retval['trck'] = u''
                if row[5]:
                    retval['tdrc'] = row[5]
                else:
                    retval['tdrc'] = u''
                if row[6]:
                    retval['tcon'] = row[6]
                else:
                    retval['tcon'] = u''
                if row[7]:
                    retval['path'] = row[7]
                else:
                    retval['path'] = u''
                if row[8]:
                    retval['tlen'] = self._format_time(row[8])
                else:
                    retval['tlen'] = u''
                if row[9]:
                    if int(row[9]) == 1:
                        retval['hid3'] = True
                else:
                    retval['hid3'] = False
                    h, t = os.path.split(retval['path'])
                    retval['tit2'] = t
                ret.append(retval)
            return ret
        except Exception, e:
            print 'collection.get_track() failed: %s\n%s\n%s\n\n' % (sql, params, e)
            return []
        
    def _format_time(self, t):
        m,s = divmod(t, 60)
        if m < 60:
            return "%02i:%02i" %(m,s)
        else:
            h,m = divmod(m, 60)
            return "%i:%02i:%02i" %(h,m,s)
