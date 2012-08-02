#!/usr/bin/env python
'''
This module is for results for photon transfer curve (PTC, aka
linearity function) analysis.


Method
------

Take 2 equal exposure files from 0sec to n sec.  Increasing exposure
time set of data that provides information about the gain
(electrons to ADU).

Results
-------

There are four HDUs:

PrimaryHDU

    No special primary HDU needed.

FileRefTableHDU

    A list of the input files that were analyzed.

PtcAmpTableHDU

    A per-amplifier table of measured quantites.

PtcColdSpotTableHDU

    A per cold spot table characterizing area of low response.

PTC Classes
-----------
'''

import base as pyfits
import common

class PtcAmpTableHDU(pyfits.BinTableHDU):
    '''
    A table HDU holding the per-amplifier results.
    '''

    #: One column for each per-amplifier measurement
    required_columns = [
        ('LinearGain','E','Linear gain measuremnt'),
        ('MedianGain','E','Gain from median method'),
        ('OverScanNoise','E','Noise from overscan method'),
        ('StdDevNoise','E','Noise from standard deviation'),
        ('FullWell','E','Point at which the gain curve blows up'),
        ('LinearRangeMin','E','Min where response is in linear range'),
        ('LinearRangeMAx','E','Max where response is in linear range'),
        ('PRNUTotalWhite','E','Total Photo Response Nonuniformity, white light'),
        ('PRNUTotalMid','E','Total Photo Response Nonuniformity, mid range'),
        ('PRNUCorrectedWhite','E','Corrected Photo Response Nonuniformity, white light'),
        ('PRNUCorrectedMid','E','Corrected Photo Response Nonuniformity, mid range'),
        ('LinRangeMin','E','Minimum ADU in which CCD stays within LinearSpecs'),
        ('LinRangeMax','E','Maximum ADU in which CCD stays within LinearSpecs'),
        ('LinearResponse','E','Maximum deviation from linear response in Full LinRange'),
        ]

    pass

class PtcColdSpotTableHDU(pyfits.BinTableHDU):
    '''
    A table HDU holding per-cold-spot quantities.
    '''

    #: One column for each per-cold-spot measurement
    required_columns = [
        ('AmpNum','I','Amplifier number, 1-based'),
        ('PixCount','I','Number of cold pixels'),
        ('SpotX','I', 'The X-pixel nearest to the spot center'),
        ('SpotY','I', 'The Y-pixel nearest to the spot center'),
        ]
    pass

class PtcInputFilesHDU(common.FileRefTableHDU):
    '''
    HDU to describe the input files for the PTC analysis.
    '''
    def __init__(self, data=None, header=None, name=None, **kwds):
        base = super(PtcInputFilesHDU,self)
        base.__init__(data=None, header=None, name=None, 
                      filedesc = 'Input files for the PTC analysis',**kwds)
        return



#: List of HDU schema classes for PTC
schema = [
    pyfits.PrimaryHDU,
    PtcInputFilesHDU,
    PtcAmpTableHDU,
    PtcColdSpotTableHDU,
]
