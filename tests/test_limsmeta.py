#!/usr/bin/env python
'''
Test the LIMS meta data schema
'''

import lcatr.schema
import pyfits

import os
import time
import datetime
from hashlib import sha1

test_filename = "test_limsmeta.fits"

def test_limsmeta():
    # define schema and fill it at the same time
    hdus = pyfits.HDUList([
        # primary
        lcatr.schema.limsmeta.schema[0](
            testname = 'TestLimsMetaData',
            date_obs = datetime.datetime(*time.gmtime()[:6]),
            username = os.environ.get('USER','testuser')            
            ),
        
        # SoftwareTableHDU:
        lcatr.schema.limsmeta.schema[1](
            commithash = [sha1().hexdigest(),],
            committag = ['TheGitTag',],
            repourl = ['git://github.com/brettviren/lcatr/',],
            progpath = ['test1/mainprog',],
            cmdline = ['./test1/mainprog arg1 arg2',],
            exitcode = [0,]
            ),

        # Result fits files
        lcatr.schema.limsmeta.schema[2](
            filename = [__file__,],
            sha1hash = [None],
            ),

        # Aux files
        lcatr.schema.limsmeta.schema[2](),
        ])
    hdus[2].generate()
    hdus[3].generate()

    print 'Initial creation:'
    print hdus[0].header

    print 'Validating original'
    hdus.validate()

    if os.path.exists(test_filename):
        print 'Removing preexisting file: "%s"' % test_filename
        os.remove(test_filename)
        pass
    hdus.writeto(test_filename)
    
    hdus2 = pyfits.open(test_filename)
    print 'Read in from file:'
    print hdus2[0].header

    print 'Validating copy'
    hdus2.validate()

if __name__ == '__main__':
    
    test_limsmeta()
