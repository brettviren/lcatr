#!/usr/bin/env python
'''
Some specific columns
'''

from schema import Column

FilePathColumn = Column('FileName', 'str',
                        'A file path relative to $CCDTEST_ROOT')
SHA1HashColumn = Column('SHA1Hash', 'sha1', 
                        'A SHA1 digest hash.')

if __name__ == '__main__':
    from hashlib import sha1
    shc = SHA1HashColumn()
    shc.set([sha1()])
    print shc
