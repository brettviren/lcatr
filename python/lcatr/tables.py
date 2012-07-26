#!/usr/bin/env python
'''
Some common tables
'''

from schema import Table
import columns
from hashlib import sha1

class PathHashTable(Table):
    def __init__(self,filelist = None, sha1list = None):

        if filelist and not sha1list:
            sha1list = [sha1(open(f).read()) for f in filelist]
            pass
        fpc = columns.FilePathColumn(filelist)
        shc = columns.SHA1HashColumn(sha1list)

        base = super(PathHashTable,self)
        base.__init__([fpc,shc])
        return
    pass

if __name__ == '__main__':
    pht = PathHashTable()
    print pht
