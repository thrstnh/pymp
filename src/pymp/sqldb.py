#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time
import os.path
from pymp.config import cfg, DEBUG, DB_FILE, DROP_ID
from pymp.config import tbl
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

dbfp = cfg[DB_FILE]
conn = sqlite3.connect(dbfp)
sqlc = conn.cursor()


def now():
    ''' timestamp '''
    return int(time.time())

def create_tables():
    # collection
    sql = u'''
        CREATE TABLE IF NOT EXISTS collection (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            dateadd INTEGER NOT NULL,
            datechg INTEGER NOT NULL,
            PRIMARY KEY(id),
            UNIQUE(name),
            UNIQUE(path) );'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

#    # init dropped collection for droped from filesystem
#    sql = r'''
#    INSERT INTO collection (name, path, dateadd, datechg)
#        VALUES ("%s", "%s", %d, %d);''' % ('dropped', '', now(), now())
#    try:
#        sqlc.execute(sql)
#    except Exception, e:
#        print "err: %s" % sql

    # artist
    sql = u'''
        CREATE TABLE IF NOT EXISTS artist (
            id INTEGER NOT NULL,
            collection_id INTEGER NOT NULL,
            tpe1 TEXT NULL,
            tpe2 TEXT NULL,
            dateadd INTEGER NOT NULL,
            datechg INTEGER NOT NULL,
            PRIMARY KEY (id) );'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    # index on artist.tpe1
    sql = '''CREATE INDEX IF NOT EXISTS speedup_TPE1 on artist(tpe1)'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql
        
    # album
    sql = u'''
        CREATE TABLE IF NOT EXISTS album (
            id INTEGER NOT NULL,
            collection_id INTEGER NOT NULL,
            talb TEXT NOT NULL,
            tpos TEXT NULL,
            tdrc TEXT NULL,
            dateadd INTEGER NOT NULL,
            datechg INTEGER NOT NULL,
            PRIMARY KEY(id) );'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    # index on album.talb
    sql = '''CREATE INDEX IF NOT EXISTS speedup_TALB on album(talb)'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    # genre
    sql = u'''
        CREATE TABLE IF NOT EXISTS genre (
            id INTEGER NOT NULL,
            tcon TEXT NOT NULL,
            dateadd INTEGER NOT NULL,
            PRIMARY KEY(id),
            UNIQUE(tcon) );'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    # lfm
    sql = u'''
        CREATE TABLE IF NOT EXISTS lfm (
            id INTEGER NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            login BOOLEAN,
            scrobble BOOLEAN,
            dateadd INTEGER NOT NULL,
            datechg INTEGER NOT NULL,
            PRIMARY KEY(id),
            UNIQUE(username) );'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    # addinfo
    sql = u'''
        CREATE TABLE IF NOT EXISTS addinfo (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            value TEXT NOT NULL,
            dateadd INTEGER NOT NULL,
            PRIMARY KEY(id) );'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    # connect track <> addinfo n:m
    sql = u'''
        CREATE TABLE IF NOT EXISTS sat_addinfo (
            track_id INTEGER NOT NULL,
            addinfo_id INTEGER NOT NULL,
            dateadd INTEGER NOT NULL);'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    # track
    sql = u'''
        CREATE TABLE IF NOT EXISTS track (
            id INTEGER NOT NULL,
            collection_id INTEGER NOT NULL,
            tit2 TEXT NOT NULL,
            path TEXT NOT NULL,
            hid3 BOOLEAN,
            artist_id INTEGER NOT NULL,
            album_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            length INTEGER NOT NULL,
            bitrate INTEGER NOT NULL,
            trck TEXT NULL,
            playcount INTEGER NOT NULL,
            playlast INTEGER NOT NULL,
            dateadd INTEGER NOT NULL,
            datechg INTEGER NOT NULL,
            PRIMARY KEY(id),
            UNIQUE(collection_id, path) );'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    # track
    sql = u'''
        CREATE TABLE IF NOT EXISTS played (
            id INTEGER NOT NULL,
            track_id INTEGER NOT NULL,
            played INTEGER NOT NULL,
            PRIMARY KEY(id));'''
    try:
        sqlc.execute(sql)
    except Exception, e:
        print "err: %s" % sql

    try:
        conn.commit()
    except Exception, e:
        print "err: commit failed"
        conn.rollback()


create_tables()

def init_collections(collections={}):
    for name, path in collections.items():
        try:
            sql = u'INSERT INTO collection (name, path, dateadd, datechg) VALUES (?, ?, ?, ?);'
            params = (name, path, now(), now())
            sqlc.execute(sql, params)
            conn.commit()
        except Exception, e:
            print "init_collections failed: %s\n%s\n%s" % (sql, e, params)

def get_collections():
    ret = {}
    try:
        sql = u'''SELECT id, name, path, dateadd, datechg
                    FROM collection
                    WHERE 1
                    ORDER BY id; '''
        sqlc.execute(sql)
        for row in sqlc:
            d = {}
            d['id'] = row[0]
            d['name'] = row[1]
            d['path'] = row[2]
            d['dateadd'] = row[3]
            d['datechg'] = row[4]
            ret[row[0]] = d
        return ret
    except Exception, e:
        print "err:get_collections: %s %s" % (sql, e)
    return ret


def get_collection_id(collection=''):
    cid = 0
    if collection:
        try:
            sql = u'SELECT id FROM collection WHERE name = ?;'
            params = collection,
            sqlc.execute(sql, params)
            cid = sqlc.fetchone()[0]
        except Exception, e:
            print u"get_collection_id: %s" % sql
    return cid

def escape(msg):
    return msg.replace(r'"', r'""')

def get_track_id(path):
    trackid = 0
    try:
        sql = u'SELECT id FROM track WHERE path = ?;'
        params = path,
        sqlc.execute(sql, params)
        item = sqlc.fetchone()
        trackid = item[0]
        return trackid
    except Exception, e:
        print "err:get_track_id:failed: %s" % e
        pass
    return trackid

def get_track(path):
#    path = path.decode('utf-8')
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
                WHERE path = ?;'''
    #print sql
    try:
        params = path,
        sqlc.execute(sql, params)
        ret = {}
        for row in sqlc:
            retval = []
            if row[0]:
                retval.append(row[0])
            else:
                retval.append(u'')
            if row[1]:
                retval.append(row[1])
            else:
                retval.append(u'')
            if row[2]:
                retval.append(row[2])
            else:
                retval.append(u'')
            if row[3]:
                retval.append(row[3])
            else:
                retval.append(u'')
            if row[4]:
                retval.append(_fix_trck(row[4]))
            else:
                retval.append(u'')
            if row[5]:
                retval.append(row[5])
            else:
                retval.append(u'')
            if row[6]:
                retval.append(row[6])
            else:
                retval.append(u'')
            if row[7]:
                retval.append(row[7])
            else:
                retval.append(u'')
            if row[8]:
                retval.append(_format_time(row[8]))
            else:
                retval.append(u'')
            if row[9]:
                if int(row[9]) == 1:
                    retval.append(True)
            else:
                retval.append(False)
                h, t = os.path.split(retval['path'])
                retval[2] = t
            ret = {retval[3] : retval}
        return ret
    except Exception, e:
        print 'sqldb.get_track() failed: %s\n%s\n%s\n\n' % (sql, params, e)
        return {}

def _format_time(t):
    m,s = divmod(t, 60)
    if m < 60:
        return "%02i:%02i" %(m,s)
    else:
        h,m = divmod(m, 60)
        return "%i:%02i:%02i" %(h,m,s)

def _init_tbl_columns():
    columns = []
    for k,v in tbl.items():
        if v[0]:
            columns.append((v[1], k))
    return [hdr for (id,hdr) in sorted(columns)]

def lfm_user(username='', md5password='', login=False, scrobble=False):
    ret = {}
    try:
        sql = u'''   SELECT
                        username, password, login,
                        scrobble, dateadd, datechg
                    FROM lfm
                    WHERE 1
                    ORDER BY id;'''
        sqlc.execute(sql)
        item = sqlc.fetchone()
        ret['username'] = item[0]
        ret['password'] = item[1]
        ret['login'] = item[2]
        ret['scrobble'] = item[3]
        ret['dateadd'] = item[4]
        ret['datechg'] = item[5]
        return ret
    except Exception, e:
        pass
    
    if login:
        login = 1
    else:
        login = 0
    
    if scrobble:
        scrobble = 1
    else:
        scrobble = 0
        
    try:
        sql = u'''
        INSERT INTO lfm (username, password, login, scrobble, dateadd, datechg)
            VALUES (?, ?, ?, ?, ?, ?);'''
        params = (username, md5password, login, scrobble, now(), now())
        sqlc.execute(sql, params)
        conn.commit()
        return lfm_user(username, md5password, login, scrobble)
    except Exception, e:
        print "err:lfm_user: insert and commit failed: %s\n  %s" % (sql, e)

def filter(cid, path, pattern, ids, kwargs):
    #path = escape(path)
    ret = {}
    params = list()
    sql = u''' SELECT
                track.id, track.tit2, track.path,
                track.length, track.trck, track.playcount,
                track.playlast, track.dateadd,
                artist.tpe1,
                album.talb, album.tdrc,
                genre.tcon
                
                FROM track
                LEFT JOIN artist
                    ON track.artist_id = artist.id
                        AND track.collection_id = artist.collection_id
                LEFT JOIN album
                    ON track.album_id = album.id
                        AND track.collection_id = album.collection_id
                LEFT JOIN genre
                    ON track.genre_id = genre.id '''
    if path:
        params.append(path)
        sql += ' WHERE path = ? '
    else:
        if any([cid, ids, pattern]):
            sql += ' WHERE '
        if cid:
            params.append(cid)
            sql += ' track.collection_id = ? '
#        if ids:
#            if cid:
#                sql += ' AND '
#            sql += '\n  track.id IN (%s) ' % strids
        if pattern:
            sql += '\n AND '
        if ' ' in pattern:
            i = 0
            for item in pattern.split(' '):
                if len(item) > 0:
                    if i > 0:
                        sql += '\n  AND \n'
                    sql += '     (track.tit2 LIKE "%' + item + '%" \n'
                    sql += '    OR artist.tpe1 LIKE "%' + item + '%" \n'
                    sql += '    OR track.path LIKE "%' + item + '%" \n'
                    sql += '    OR album.talb LIKE "%' + item + '%" \n'
                    sql += '    OR genre.tcon LIKE "%' + item + '%") \n'
                    i += 1
        if ' ' not in pattern and len(pattern) > 0:
            sql += '\n    (track.tit2 LIKE "%' + pattern + '%" \n'
            sql += '     OR artist.tpe1 LIKE "%' + pattern + '%" \n'
            sql += '     OR track.path LIKE "%' + pattern + '%" \n'
            sql += '     OR album.talb LIKE "%' + pattern + '%" \n'
            sql += '     OR genre.tcon LIKE "%' + pattern + '%") \n'
    #print sql
    try:
        sqlc.execute(sql, params)
        for row in sqlc:
            td = []
            td.append(row[0]) # ID
            if row[1]:
                td.append(row[1])
            else:
                td.append(u'') # TIT2
            if row[8]:
                td.append(row[8])
            else:
                td.append(u'')
            if row[9]:
                td.append(row[9])
            else:
                td.append(u'')
            if row[11]:
                td.append(row[11])
            else:
                td.append(u'')
            if row[10]:
                td.append(row[10])
            else:
                td.append(u'')
            if row[3]:
                td.append(_format_time(int(round(float(row[3]))))) # TLEN
            else:
                td.append(0)
            if row[4]:
                td.append(_fix_trck(row[4]))
            else:
                td.append(u'')
            if row[2]:
                td.append(row[2])
            else:
                td.append(u'')
            ret[row[0]] = td
    except Exception, e:
        print "err:filter: %s\n  %s" % (sql, e)
    return ret

def qt_model_filter(cid, path, pattern, ids, kwargs):
    #path = escape(path)
    ret = []
    params = list()
    sql = u''' SELECT
                track.id, track.tit2, track.path,
                track.length, track.trck, track.playcount,
                track.playlast, track.dateadd,
                artist.tpe1,
                album.talb, album.tdrc,
                genre.tcon

                FROM track
                LEFT JOIN artist
                    ON track.artist_id = artist.id
                        AND track.collection_id = artist.collection_id
                LEFT JOIN album
                    ON track.album_id = album.id
                        AND track.collection_id = album.collection_id
                LEFT JOIN genre
                    ON track.genre_id = genre.id '''
    if path:
        params.append(path)
        sql += ''' WHERE path = ? '''
    else:
        if any([cid, ids, pattern]):
            sql += ' WHERE '
        if cid:
            params.append(cid)
            sql += ' track.collection_id = ? '
#        if ids:
#            if cid:
#                sql += ' AND '
#            sql += '\n  track.id IN (%s) ' % strids
        if pattern:
            sql += '\n AND '
        if ' ' in pattern:
            i = 0
            for item in pattern.split(' '):
                if len(item) > 0:
                    if i > 0:
                        sql += '\n  AND \n'
                    sql += '     (track.tit2 LIKE "%' + item + '%" \n'
                    sql += '    OR artist.tpe1 LIKE "%' + item + '%" \n'
                    sql += '    OR track.path LIKE "%' + item + '%" \n'
                    sql += '    OR album.talb LIKE "%' + item + '%" \n'
                    sql += '    OR genre.tcon LIKE "%' + item + '%") \n'
                    i += 1
        if ' ' not in pattern and len(pattern) > 0:
            sql += '\n    (track.tit2 LIKE "%' + pattern + '%" \n'
            sql += '     OR artist.tpe1 LIKE "%' + pattern + '%" \n'
            sql += '     OR track.path LIKE "%' + pattern + '%" \n'
            sql += '     OR album.talb LIKE "%' + pattern + '%" \n'
            sql += '     OR genre.tcon LIKE "%' + pattern + '%") \n'
    #print sql
    try:
        sqlc.execute(sql, params)
        for row in sqlc:
            td = []
            td.append(QtCore.QString("%1").arg(row[0])) # ID
            if row[1]:
                td.append(QtCore.QString("%1").arg(row[1])) # TIT2
            else:
                td.append(QtCore.QString("%1").arg('')) # TIT2
            if row[8]:
                td.append(QtCore.QString("%1").arg(row[8])) # TPE1
            else:
                td.append(QtCore.QString("%1").arg(''))
            if row[9]:
                td.append(QtCore.QString("%1").arg(row[9]))
            else:
                td.append(QtCore.QString("%1").arg(''))
            if row[11]:
                td.append(QtCore.QString("%1").arg(row[11])) # TCON
            else:
                td.append(QtCore.QString("%1").arg(''))
            if row[10]:
                td.append(QtCore.QString("%1").arg(row[10])) # TDRC
            else:
                td.append(QtCore.QString("%1").arg(''))
            if row[3]:
                td.append(QtCore.QString("%1").arg(_format_time(int(round(float(row[3])))))) # TLEN
            else:
                td.append(QtCore.QString("%1").arg(0))
            if row[4]:
                td.append(QtCore.QString("%1").arg(_fix_trck(row[4]))) # TRCK
            else:
                td.append(QtCore.QString("%1").arg(''))
            if row[2]:
                td.append(QtCore.QString("%1").arg(row[2])) # PATH
            else:
                td.append(QtCore.QString("%1").arg(''))
            ret.append(td)
    except Exception, e:
        print "err:filter: %s\n  %s" % (sql, e)
    return ret

def tree(cid, pattern=''):
    sql = u'''SELECT artist.tpe1, album.talb, track.tit2, track.id, track.trck, album.tdrc
                FROM track
                LEFT JOIN artist
                    ON track.artist_id = artist.id
                LEFT JOIN album
                    ON track.album_id = album.id
                WHERE track.collection_id = '%s'
                        AND album.collection_id = '%s'
                        AND artist.collection_id = '%s' ''' % (cid, cid, cid)

    if pattern and len(pattern) > 0:
        sql += '\n   AND (track.tit2 LIKE "%' + pattern + '%" \n'
        sql += '     OR artist.tpe1 LIKE "%' + pattern + '%" \n'
        sql += '     OR track.path LIKE "%' + pattern + '%" \n'
        sql += '     OR album.talb LIKE "%' + pattern + '%") \n'
        
    sql += '''  ORDER BY artist.tpe1, album.tdrc, album.talb, track.trck
                ASC''' 
    #print sql
    try:
        sqlc.execute(sql)
        ret = []
        for row in sqlc:
            td = []
            if row[0]:
                td.append(row[0].encode('utf-8'))
            else:
                td.append('')
            if row[1]:
                if row[5]:
                    td.append('%s %s'.encode('utf-8') % (row[5], row[1]))
                else:
                    td.append(row[1].encode('utf-8'))
            else:
                td.append('')
            if row[2]:
                if row[4]:
                    td.append('%s %s'.encode('utf-8') % (_fix_trck(row[4]), row[2]))
                else:
                    td.append('%s'.encode('utf-8') % row[2])
            else:
                td.append('')
            if row[3]:
                td.append(row[3])
            else:
                td.append(0)
            ret.append(td)
        return ret
    except Exception, e:
        print 'sql.tre_set_artists() failed: %s\n  %s' % (sql, e)
        return []

def count_collection(cid):
    cnt = 0
    try:
        sql = sql = u'SELECT COUNT(*) FROM track WHERE collection_id = ?'
        params = cid,
        sqlc.execute(sql, params)
        item = sqlc.fetchone()
        cnt = item[0]
        return cnt
    except Exception, e:
        print "err:count_collection:failed: %s" % e
        pass
    return cnt

def count_collection_tracks(cid):
    cnt = 0
    try:
        sql = u'SELECT COUNT(*) FROM track WHERE collection_id = ?'
        params = cid,
        sqlc.execute(sql, params)
        item = sqlc.fetchone()
        cnt = item[0]
        return cnt
    except Exception, e:
        print "err:count_collection_tracks:failed: %s" % e
    return cnt


def count_tracks():
    cnt = 0
    try:
        sql = u'SELECT COUNT(*) FROM track'
        sqlc.execute(sql)
        item = sqlc.fetchone()
        cnt = item[0]
        return cnt
    except Exception, e:
        print "err:count_tracks:failed: %s" % e
    return cnt

def count_artist_files(cid, artist):
    cnt = 0
    try:
        sql = u'''SELECT COUNT(*) FROM track
                        LEFT JOIN artist
                            ON track.artist_id = artist.id
                        WHERE artist.tpe1 = ?
                            AND track.collection_id = ?;'''
        params = (artist, cid)
        sqlc.execute(sql, params)
        item = sqlc.fetchone()
        cnt = item[0]
        return cnt
    except Exception, e:
        print "err:count_artist_files:failed: %s" % e
    return cnt
    

def tree_dict(cid, pattern=''):
    params = list()
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
                WHERE track.collection_id = ? '''
    params.append(cid)

#    if pattern and len(pattern) > 0:
#        sql += '\n   AND (track.tit2 LIKE "%' + pattern + '%" \n'
#        sql += '     OR artist.tpe1 LIKE "%' + pattern + '%" \n'
#        sql += '     OR track.path LIKE "%' + pattern + '%" \n'
#        sql += '     OR album.talb LIKE "%' + pattern + '%") \n'
    if pattern:
        sql += '\n AND '
    if ' ' in pattern:
        i = 0
        for item in pattern.split(' '):
            if len(item) > 0:
                if i > 0:
                    sql += '\n  AND \n'
                sql += '     (track.tit2 LIKE "%' + item + '%" \n'
                sql += '    OR artist.tpe1 LIKE "%' + item + '%" \n'
                sql += '    OR track.path LIKE "%' + item + '%" \n'
                sql += '    OR album.talb LIKE "%' + item + '%" \n'
                sql += '    OR genre.tcon LIKE "%' + item + '%") \n'
                i += 1
    if ' ' not in pattern and len(pattern) > 0:
        sql += '\n    (track.tit2 LIKE "%' + pattern + '%" \n'
        sql += '     OR artist.tpe1 LIKE "%' + pattern + '%" \n'
        sql += '     OR track.path LIKE "%' + pattern + '%" \n'
        sql += '     OR album.talb LIKE "%' + pattern + '%" \n'
        sql += '     OR genre.tcon LIKE "%' + pattern + '%") \n'



    sql += '''  ORDER BY artist.tpe1, album.tdrc, album.talb, track.trck
                ASC'''
    #print sql
    try:
        sqlc.execute(sql, params)
        ret = []
        for row in sqlc:
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
                retval['trck'] = _fix_trck(row[4])
            else:
                retval['trck'] = u''
            if row[5]:
                if u'-' in row[5]:
                    retval['tdrc'] = row[5].split('-')[0]
                else:
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
                retval['tlen'] = _format_time(row[8])
            else:
                retval['tlen'] = u''
            if row[9]:
                if int(row[9]) == 1:
                    retval['hid3'] = True
            else:
                retval['hid3'] = False
                h, t = os.path.split(retval['path'])
                retval['tit2'] = t
            #else:
            ret.append(retval)
        return ret
    except Exception, e:
        print 'sql.tree_dict() failed: %s\n%s\n%s\n\n' % (sql, params, e)
        return []

def qt_tree_dict(cid, pattern=''):
    params = list()
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
                WHERE track.collection_id = ? '''
    params.append(cid)

#    if pattern and len(pattern) > 0:
#        sql += '\n   AND (track.tit2 LIKE "%' + pattern + '%" \n'
#        sql += '     OR artist.tpe1 LIKE "%' + pattern + '%" \n'
#        sql += '     OR track.path LIKE "%' + pattern + '%" \n'
#        sql += '     OR album.talb LIKE "%' + pattern + '%") \n'
    if pattern:
        sql += '\n AND '
    if ' ' in pattern:
        i = 0
        for item in pattern.split(' '):
            if len(item) > 0:
                if i > 0:
                    sql += '\n  AND \n'
                sql += '     (track.tit2 LIKE "%' + item + '%" \n'
                sql += '    OR artist.tpe1 LIKE "%' + item + '%" \n'
                sql += '    OR track.path LIKE "%' + item + '%" \n'
                sql += '    OR album.talb LIKE "%' + item + '%" \n'
                sql += '    OR genre.tcon LIKE "%' + item + '%") \n'
                i += 1
    if ' ' not in pattern and len(pattern) > 0:
        sql += '\n    (track.tit2 LIKE "%' + pattern + '%" \n'
        sql += '     OR artist.tpe1 LIKE "%' + pattern + '%" \n'
        sql += '     OR track.path LIKE "%' + pattern + '%" \n'
        sql += '     OR album.talb LIKE "%' + pattern + '%" \n'
        sql += '     OR genre.tcon LIKE "%' + pattern + '%") \n'



    sql += '''  ORDER BY artist.tpe1, album.tdrc, album.talb, track.trck
                ASC'''
    #print sql
    try:
        sqlc.execute(sql, params)
        ret = []
        for row in sqlc:
            retval = {}
            if row[0]:
                retval['tpe1'] = QString(row[0])
            else:
                retval['tpe1'] = QtCore.QString("%1").arg('')
            if row[1]:
                retval['talb'] = QtCore.QString("%1").arg(row[1])
            else:
                retval['talb'] = QtCore.QString("%1").arg('')
            if row[2]:
                retval['tit2'] = QtCore.QString("%1").arg(row[2])
            else:
                retval['tit2'] = QtCore.QString("%1").arg('')
            if row[3]:
                retval['tid'] = QtCore.QString("%1").arg(row[3])
            else:
                retval['tid'] = QtCore.QString("%1").arg('')
            if row[4]:
                #print "b: %s \ta: %s" % (row[4].encode('utf-8'), _fix_trck(row[4].encode('utf-8')))
                retval['trck'] = QtCore.QString("%1").arg(_fix_trck(row[4]))
            else:
                retval['trck'] = QtCore.QString("%1").arg('')
            if row[5]:
                retval['tdrc'] = QtCore.QString("%1").arg(row[5])
            else:
                retval['tdrc'] = QtCore.QString("%1").arg('')
            if row[6]:
                retval['tcon'] = QtCore.QString("%1").arg(row[6])
            else:
                retval['tcon'] = QtCore.QString("%1").arg('')
            if row[7]:
                retval['path'] = QtCore.QString("%1").arg(row[7])
            else:
                retval['path'] = QtCore.QString("%1").arg('')
            if row[8]:
                retval['tlen'] = QtCore.QString("%1").arg(_format_time(row[8]))
            else:
                retval['tlen'] = ''
            if row[9]:
                if int(row[9]) == 1:
                    retval['hid3'] = True
            else:
                retval['hid3'] = False
                h, t = os.path.split(retval['path'])
                retval['tit2'] = t
            #else:
            ret.append(retval)
        return ret
    except Exception, e:
        print 'sql.tree_dict() failed: %s\n%s\n%s\n\n' % (sql, params, e)
        return []

def play_track(tid=0):
    if tid > 0 and tid < cfg[DROP_ID]:
        sql = u'''INSERT INTO played (track_id, played)
                    VALUES (?, ?)'''
        try:
            params = (tid, now())
            sqlc.execute(sql, params)
            conn.commit()
        except Exception, e:
            print 'sqldb.play_track() failed: %s\n  %s' % (sql, e)

def delete_track(path):
    sql = u'DELETE FROM track WHERE PATH = ?'
    params = path,
    sqlc.execute(sql, params)
    conn.commit()

def delete_collection(cid):
    sql = u'DELETE FROM artist WHERE collection_id = ?;'
    try:
        params = cid,
        sqlc.execute(sql, params)
        conn.commit()
    except Exception, e:
        print 'delete_collection::artist failed: %s\n  %s' % (sql, e)
    
    sql = u'DELETE FROM album WHERE collection_id = ?;'
    try:
        params = cid,
        sqlc.execute(sql, params)
        conn.commit()
    except Exception, e:
        print 'delete_collection::album failed: %s\n  %s' % (sql, e)

    sql = u'DELETE FROM track WHERE collection_id = ?;'
    try:
        params = cid,
        sqlc.execute(sql, params)
        conn.commit()
    except Exception, e:
        print 'delete_collection::track failed: %s\n  %s' % (sql, e)
        
    sql = u'DELETE FROM collection WHERE id = ?;'
    try:
        params = cid,
        sqlc.execute(sql, params)
        conn.commit()
    except Exception, e:
        print 'delete_collection::track failed: %s\n  %s' % (sql, e)


def _fix_trck(trck):
    if len(trck) == 1:
        if trck == '0':
            trck = ''
        else:
            trck = '0%s' % trck
    elif trck.find('/') > 0:
        tpart, tnum = trck.split('/')
        if len(tpart) == 1:
            tpart = '0%s' % tpart
        if len(tnum) == 1:
            tnum = '0%s' % tnum
        trck = '%s/%s' % (tpart, tnum)
    return trck
