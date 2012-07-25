#!/usr/bin/env python
'''
Some specific columns
'''

from schema import Column

class FilePathColumn(Column):
    def __init__(self, filelist = None):
        base = super(FilePathColumn,self)
        base.__init__('FilePath', 'str', 'A file path',filelist)
        return
    pass

class SHA1HashColumn(Column):
    def __init__(self, sha1list = None):
        base = super(SHA1HashColumn,self)
        base .__init__('SHA1Hash', 'sha1', 'A SHA1 digest hash.',sha1list)
        return
    pass

if __name__ == '__main__':
    from hashlib import sha1
    shc = SHA1HashColumn()
    shc.set([sha1()])
    print shc
