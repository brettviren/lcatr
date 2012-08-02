#!/usr/bin/env python
'''
Some common, reusable HDU classes.
'''

import base as pyfits
import util

class FileRefTableHDU(pyfits.BinTableHDU):
    '''
    A table HDU containing references to files.

    The named keywords are passed up to the parrent class.  All
    remaining keyword arguments, if any, are used to initialize the
    columns as described below.

    '''
    
    #: Required cards to describe the collection of file references
    required_cards = [
        ('FileDesc','Description of the collection of referenced files'),
        ]

    #: Required columns to described file references.
    required_columns = [
        ('FileName', 'A64','The referenced file paths.'), 
        ('SHA1Hash', 'A64', 'A SHA1 digest of the file contents'),
        ]


    def generate(self):
        '''
        Replace file hashes with new ones by running
        ``hashlib.sha1()`` on the file contents.
        '''
        hashes = []
        for filename,ignore in self.data:
            h = util.sha1_digest(filename)
            if not h:
                raise ValueError,'FileRefTableHDU.generate() failed take SHA1 of "%s"' % filename
            hashes.append(h.hexdigest())
            continue
        self.set_column_array('SHA1Hash',hashes)
        return

    def validate(self):
        '''
        Validate the referenced files.

        This will locate each file by its path and calculate the SHA1
        hash of its contents.

        See util.full_path() for how the files are located.
        '''
        for name,digest in self.data:
            h = util.sha1_digest(name)
            if not h:
                raise ValueError,'Failed to take SHA1 of "%s"' % name
            h = h.hexdigest()
            if h != digest:
                raise ValueError,'SHA1 hash mismatch for "%s": %s != %s' % (name, h, digest)
            continue
        return
    pass

if __name__ == '__main__':
    frt = FileRefTableHDU(filename=[__file__],sha1hash=[None])
    try:
        frt.validate()
    except ValueError,msg:
        print msg
        print 'Caught expected error, continue'
    else: raise
    print 'Before generate():\n', frt.data
    frt.generate()
    print 'After generate():\n', frt.data
    print 'Validating, should succeed:'
    frt.validate()


    
