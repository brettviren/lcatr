#!/usr/bin/env python
'''
Common HDUs
'''

import schema
import headers
import columns
import tables

class PrimaryHDU(schema.HDU):
    '''
    The primary HDU.
    '''
    def __init__(self,station_name):
        ph = headers.PrimaryHeader(station_name)
        super(PrimaryHDU,self).__init__(ph)
        return
    pass

class FileRefHDU(schema.HDU):
    '''
    An HDU for storing references to files.

    An optional list of filehashes can be passed.  The list are
    doubles holding a path and either a hashlib.sha1() or a SHA1
    digest string in hex.
    '''
    def __init__(self, filelist, sha1list = None):
        mh = headers.MinimalHeader('FileRefs')
        pht = tables.PathHashTable(filelist, sha1list)
        super(FileRefHDU,self).__init__(mh,[pht])
        return
    pass

if '__main__' == __name__:
    phdu = PrimaryHDU('ATestResult')
    print phdu

    frhdu = FileRefHDU([__file__])
    print frhdu

