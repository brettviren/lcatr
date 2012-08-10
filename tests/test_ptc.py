#!/usr/bin/env python
'''
Test making a PTC FITS file.
'''
import os
import lcatr.schema
import pyfits

import time
import datetime

import test_ptc_data as tpd

test_filename = "test_ptc.fits"

def test_ptc():

    hdus = pyfits.HDUList([
            
        # primary hdu
        lcatr.schema.ptc.schema[0](
                testname = 'TestPTC',
                date_obs = datetime.datetime(*time.gmtime()[:6]),
                username = os.environ.get('USER','testuser')            
                ),
        
        # input files
        lcatr.schema.ptc.schema[1](
                filename = [__file__,], # fake it
                sha1hash = [None]
                ),

        # per-amp numbers
        lcatr.schema.ptc.schema[2](
                lineargain = tpd.LinearGain,
                mediangain = tpd.MedianGain,
                overscannoise = tpd.OverScanNoise,
                stddevnoise = tpd.StdDevNoise,
                fullwell = tpd.FullWell,
                linearrangemin = tpd.LinearRangeMin,
                linearrangemax = tpd.LinearRangeMax,
                prnutotal = tpd.PRNUTotal,
                prnucorrected = tpd.PRNUCorrected,
                linrangemin = tpd.LinRangeMin,
                linrangemax = tpd.LinRangeMax,
                linearresponse = tpd.LinearResponse
                ),
        
        # cold spots
        lcatr.schema.ptc.schema[3](
                ampnum = tpd.ampnum,
                pixcount = tpd.pixcount,
                spotx = tpd.spotx,
                spoty = tpd.spoty
                ),

                ])              # end HDUlist

    hdus[1].generate()

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

    test_ptc()
