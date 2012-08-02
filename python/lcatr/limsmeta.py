#!/usr/bin/env python
'''
Schema for the LIMS Metadata file.

This consists of four HDUs as listed in the ``lcatr.limsmeta.schema``
variable below.
'''

import base as pyfits
import common

class LimsMetaPrimaryHDU(pyfits.PrimaryHDU):
    '''
    Primary HDU for LIMS Metadata file.

    This HDU holds meta information about the test itself.

    All named keywords are passed to the ``pyfits`` PrimaryHDU.  Any
    remaining keywords are interpreted as card values.  See below for
    the required cards.
    '''

    #: Additional required cards for LIMS Meta data primary HDU
    required_cards = [
        ('TESTNAME','Canonical name for the test result'),
        ('DATE-OBS','Time stamp of when test is run'),
        ('USERNAME','Name of operator/analyzer performing test'),
        ]
    pass

class LimsMetaResultFilesHDU(common.FileRefTableHDU):
    '''
    HDU to describe the test summary result files.
    '''
    def __init__(self, data=None, header=None, name=None, **kwds):
        base = super(LimsMetaResultFilesHDU,self)
        base.__init__(data=None, header=None, name=None, 
                      filedesc = 'Result FITS files for parsing into the database',**kwds)
        return

class LimsMetaAuxiliaryFilesHDU(common.FileRefTableHDU):
    '''
    HDU to describe the test auxiliary result files.
    '''
    def __init__(self, data=None, header=None, name=None, **kwds):
        base = super(LimsMetaResultFilesHDU,self)
        base.__init__(data=None, header=None, name=None, 
                      filedesc = 'Auxiliary files from the test',**kwds)
        return



class LimsMetaSoftwareTableHDU(pyfits.BinTableHDU):
    '''
    Table HDU describing software that was run to produce a test result.
    '''
    #: The required columns to describe the running of the testing software.
    required_columns = [
        ('CommitHash','A64', 'The SHA1 hash of the GIT commit providing the software'), 
        ('CommitTag', 'A64', 'The corresponding GIT commit tag'),   
        ('RepoURL', 'A64', 'The URL pointing at the GIT repository'),  
        ('ProgPath', 'A64', 'Path rooted in the repository to the main program'),   
        ('CmdLine', 'A64', 'The command line argument string given to the main program'),    
        ('ExitCode', 'J', 'The exit return code'),
        ]
    pass

#: The schema for a LIMS meta data file in the form of a list of HDU classes.
#: In addition to the primary there are:
#: 
#: 1) ``lcatr.limsmeta.SoftwareTableHDU`` software descripion in the form of a GIT SHA1 commit has, tag and program name
#: 
#: 2) ``lcatr.common.FileRefTableHDU``, describing Result FITS files to be parsed into LIMS
#: 
#: 3) ``lcatr.common.FileRefTableHDU``, describing any auxiliary files to be linked into LIMS database
schema = [
    LimsMetaPrimaryHDU,
    LimsMetaSoftwareTableHDU,
    LimsMetaResultFilesHDU,
    LimsMetaAuxiliaryFilesHDU
    ]


