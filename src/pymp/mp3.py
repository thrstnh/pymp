#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.mp3 import *

id3_frames = {
        #http://en.wikipedia.org/wiki/ID3
        #ID3v2 Frame Specification (Version 2.3)
            'AENC' : 'Audio encryption',
            'APIC' : 'Attached picture',
            'COMM' : 'Comments',
            'COMR' : 'Commercial frame',
            'ENCR' : 'Encryption method registration',
            'EQUA' : 'Equalization (replaced by EQU2 in v2.4)',
            'ETCO' : 'Event timing codes',
            'GEOB' : 'General encapsulated object',
            'GRID' : 'Group identification registration',
            'IPLS' : 'Involved people list (replaced by TMCL and TIPL in v2.4)',
            'LINK' : 'Linked information',
            'MCDI' : 'Music CD identifier',
            'MLLT' : 'MPEG location lookup table',
            'OWNE' : 'Ownership frame',
            'PRIV' : 'Private frame',
            'PCNT' : 'Play counter',
            'POPM' : 'Popularimeter',
            'POSS' : 'Position synchronisation frame',
            'RBUF' : 'Recommended buffer size',
            'RVAD' : 'Relative volume adjustment (replaced by RVA2 in v2.4)',
            'RVRB' : 'Reverb',
            'SYLT' : 'Synchronized lyric/text',
            'SYTC' : 'Synchronized tempo codes',
            'TALB' : 'Album/Movie/Show title',
            'TBPM' : 'BPM (beats per minute)',
            'TCOM' : 'Composer',
            'TCON' : 'Content type',
            'TCOP' : 'Copyright message',
            'TDAT' : 'Date (replaced by TDRC in v2.4)',
            'TDLY' : 'Playlist delay',
            'TENC' : 'Encoded by',
            'TEXT' : 'Lyricist/Text writer',
            'TFLT' : 'File type',
            'TIME' : 'Time (replaced by TDRC in v2.4)',
            'TIT1' : 'Content group description',
            'TIT2' : 'Title/songname/content description',
            'TIT3' : 'Subtitle/Description refinement',
            'TKEY' : 'Initial key',
            'TLAN' : 'Language(s)',
            'TLEN' : 'Length',
            'TMED' : 'Media type',
            'TOAL' : 'Original album/movie/show title',
            'TOFN' : 'Original filename',
            'TOLY' : 'Original lyricist(s)/text writer(s)',
            'TOPE' : 'Original artist(s)/performer(s)',
            'TORY' : 'Original release year (replaced by TDOR in v2.4)',
            'TOWN' : 'File owner/licensee',
            'TPE1' : 'Lead performer(s)/Soloist(s)',
            'TPE2' : 'Band/orchestra/accompaniment',
            'TPE3' : 'Conductor/performer refinement',
            'TPE4' : 'Interpreted, remixed, or otherwise modified by',
            'TPOS' : 'Part of a set',
            'TPUB' : 'Publisher',
            'TRCK' : 'Track number/Position in set',
            'TRDA' : 'Recording dates (replaced by TDRC in v2.4)',
            'TRSN' : 'Internet radio station name',
            'TRSO' : 'Internet radio station owner',
            'TSIZ' : 'Size (deprecated in v2.4)',
            'TSRC' : 'ISRC (international standard recording code)',
            'TSSE' : 'Software/Hardware and settings used for encoding',
            'TYER' : 'Year (replaced by TDRC in v2.4)',
            'TXXX' : 'User defined text information frame',
            'UFID' : 'Unique file identifier',
            'USER' : 'Terms of use',
            'USLT' : 'Unsychronized lyric/text transcription',
            'WCOM' : 'Commercial information',
            'WCOP' : 'Copyright/Legal information',
            'WOAF' : 'Official audio file webpage',
            'WOAR' : 'Official artist/performer webpage',
            'WOAS' : 'Official audio source webpage',
            'WORS' : 'Official internet radio station homepage',
            'WPAY' : 'Payment',
            'WPUB' : 'Publishers official webpage',
            'WXXX' : 'User defined URL link frame',
        #ID3v2 Frame Specification (Version 2.4 - delta respect to 2.3)
            'EQUA' : 'replaced by the EQU2 frame',
            'IPLS' : 'replaced by the two frames TMCL and TIPL',
            'RVAD' : 'replaced by the RVA2 frame',
            'TDAT' : 'replaced by the TDRC frame',
            'TIME' : 'replaced by the TDRC frame',
            'TORY' : 'replaced by the TDOR frame',
            'TRDA' : 'replaced by the TDRC frame',
            'TYER' : 'replaced by the TDRC frame',
            'TSIZ' : 'deprecated.',
        #NEW FRAMES IN 2.4:
            'ASPI' : 'Audio seek point index',
            'EQU2' : 'Equalisation',
            'RVA2' : 'Relative volume adjustment',
            'SEEK' : 'Seek frame',
            'SIGN' : 'Signature frame',
            'TDEN' : 'Encoding time',
            'TDOR' : 'Original release time',
            'TDRC' : 'Recording time',
            'TDRL' : 'Release time',
            'TDTG' : 'Tagging time',
            'TIPL' : 'Involved people list',
            'TMCL' : 'Musician credits list',
            'TMOO' : 'Mood',
            'TPRO' : 'Produced notice',
            'TSOA' : 'Album sort order',
            'TSOP' : 'Performer sort order',
            'TSOT' : 'Title sort order',
            'TSST' : 'Set subtitle'
        }

fields = ['TPE2', 'TPE1', 'TIT1', 'TIT2', 'TALB', 'TLEN', 'TDRC', 'TRCK',
        'TENC', 'TFLT', 'TDRL', 'TLAN', 'TPUB', 'TCOP',  'TCON', 'TCOM',
        'TSSE', 'TDTG', 'TBPM', 'TPOS', 'BITR']
        
#fields = ['TDRC', 'TRCK', 'TCON', 'TIT2', 'TPE1',
#                'TPE2', 'TALB', 'TLEN', 'TPOS', 'TSSE']

class PMP3(object):
    def __init__(self, path=''):
        self._path = path

        #print "mp3: ", type(self.path), self.path

        try: self.mp3 = MP3(self._path)
        except: self.mp3 = None

        try: self.id3 = ID3(self._path)
        except: self.id3 = None

    @property
    def path(self):
        return self._path

    @property
    def is_mp3(self):
        if self.mp3: return True
        return False
    
    @property
    def has_id3(self):
        if self.id3: return True
        return False

    @property
    def length(self):
        if self.is_mp3:
            return self.mp3.info.length
        return -1

    @property
    def bitrate(self):
        if self.is_mp3:
            return self.mp3.info.bitrate
        return -1

    @property
    def artist(self):
        if self.is_mp3 and self.has_id3:
            return '%s' % self.id3.get('TPE1', '')

    @property
    def title(self):
        if self.is_mp3 and self.has_id3:
            return '%s' % self.id3.get('TIT2', '')

    @property
    def album(self):
        if self.is_mp3 and self.has_id3:
            return '%s' % self.id3.get('TALB', '')

    @property
    def comment(self):
        if self.is_mp3 and self.has_id3:
            return '%s' % self.id3.get('COMM', '')

    @property
    def genre(self):
        if self.is_mp3 and self.has_id3:
            return '%s' % self.id3.get('TCON', '')

    @property
    def trackno(self):
        if self.is_mp3 and self.has_id3:
            return '%s' % self.id3.get('TRCK', '')

    @property
    def year(self):
        if self.is_mp3 and self.has_id3:
            return '%s' % self.id3.get('TDRC', '')

    def all(self):
        if self.is_mp3 and self.has_id3:
            d = {}
            for f in fields:
                item = self.id3.get(f, '')
                if item:
                    d[f] = u"%s" % item
            d['TLEN'] = self.length
            d['BITR'] = self.bitrate or ''
            return d
        return {}

    def id3_frames(self):
        ret = dict()
        if self.is_mp3 and self.has_id3:
            
            for fkey in id3_frames:
                item = self.id3.get(fkey, '')
                if item:
                    ret[fkey] = (item, id3_frames[fkey])
            ret.update({'TLEN' : (str(self.length()), id3_frames[fkey])})
        return ret

    def __str__(self):
        return '%r \n%r' % (self.path, self.id3_frames())