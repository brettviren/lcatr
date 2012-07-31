#!/usr/bin/env python
'''
Schema for the LIMS Metadata file.
'''

import base as pyfits
import common

class LimsMetaPrimaryHDU(pyfits.PrimaryHDU):
    '''
    Primary HDU for LIMS Metadata file.

    This HDU holds basic information about the test itself.

    '''

    schema_name = 'LimsMeta'
    
    #: Required cards for LIMS Meta data primary HDU
    required_cards = [
        ('TESTNAME','Canonical name for the test result'),
        ('DATE-OBS','Time stamp of when test is run'),
        ('USERNAME','Name of operator/analyzer performing test'),
        ]
    pass

class SoftwareTableHDU(pyfits.BinTableHDU):
    '''
    Table HDU describing software run to produce a test result.

    This holds columns of:
    
    - A GIT SHA1 commit hash
    - A coresponding GIT tag label
    - ......
    '''
    fixme()
    pass

#: The schema for a LIMS meta data file.
#: 
#: This consists of four HDUs.  In addition to the primary there are:
#: 
#: 1) ``lcatr.limsmeta.SoftwareTableHDU`` software descripion in the form of a GIT SHA1 commit has, tag and program name
#: 
#: 2) ``lcatr.common.FileRefTableHDU``, describing Result FITS files to be parsed into LIMS
#: 
#: 3) ``lcatr.common.FileRefTableHDU``, describing any auxiliary files to be linked into LIMS database
schema = pyfits.HDUList([
        LimsMetaPrimaryHDU(),
        SoftwareTableHDU(),
        common.FileRefTableHDU(),
        common.FileRefTableHDU(),
        ])


if __name__ == '__main__':
    import datetime, time
    import util

    meta = LimsMetaPrimaryHDU(testname = 'TestLimsMeta')
    meta.header.update('username','theycallmedog')
    try:
        meta.validate()
    except ValueError, msg:
        print msg
        print 'Got error on validation of partial primary HDU as expected'
        pass
    now = datetime.datetime(*time.gmtime()[:6])
    meta.header['date-obs'] = util.wash_card_value(now)
    print meta.header
    meta.validate()
