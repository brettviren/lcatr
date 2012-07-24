#!/usr/bin/env python
'''
Some common tables
'''

from schema import Table
from columns import *

class PathHashTable(Table):
    def __init__(self,filelist,sha1list):
        super(PathHashTable,self).__init__(None)
        #= Table([FilePathColumn(), SHA1HashColumn()])

if __name__ == '__main__':
    print PathHashTable
    pht = PathHashTable()
    print pht
