#!/usr/bin/env python
'''
Test the GNC schema
'''

import os
import lcatr
from hashlib import sha1
import numpy as np

import test_gnc_data as tgd


def dump(gnc):
    print '''
Dumping GNC
===========
'''

    gnc.info()
    for hdu in gnc:
        msg = 'HDU: "%s"' % hdu.name
        print
        print msg
        print '-'*len(msg)
        print 'Header:'
        print hdu.header
        print 'Data:'
        print hdu.data
        continue
    return

gnc = None

def test_empty():
    global gnc
    gnc = lcatr.gnc.GncResult()
    #dump(gnc)

def test_update():
    global gnc
    
    fileRefs = gnc['FileRefs']
    fileRefs.set_column_array('FileName',tgd.analyzed_files)
    fileRefs.set_column_array('SHA1hash',[sha1().hexdigest() for x in tgd.analyzed_files])
    fileRefs.validate()
    
    gains = gnc['Gains']
    gains.set_column_array('LinGains', tgd.linear_fit_gains)
    gains.set_column_array('MedGains', tgd.median_gains)
    gains.validate()
    
    noises = gnc['Noises']
    noises.set_column_array('OvScNois', tgd.overscan_noise)
    noises.set_column_array('SdevNois', tgd.stddev_noise)
    noises.validate()

    ampnum = []
    pixcount = []
    spotx = []
    spoty = []
    for spots in tgd.cold_spots:
        n = spots[0]
        c = spots[1]
        for x,y in spots[2:]:
            ampnum.append(n)
            pixcount.append(c)
            spotx.append(x)
            spoty.append(y)
            continue
        continue
    spots = gnc['ColdSpot']
    spots.set_column_array('AmpNum', ampnum)
    spots.set_column_array('PixCount', pixcount)
    spots.set_column_array('SpotX', spotx)
    spots.set_column_array('SpotY', spoty)
    spots.validate()

    return

def test_validate():
    global gnc
    gnc.validate()

def test_write():
    '''
    Write to file 
    '''
    global gnc
    filename = "test_gnc.fits"
    if os.path.exists(filename):
        #print 'File "%s" exists, removing' % filename
        os.remove(filename)
        pass
    gnc.writeto(filename)

def test_read_and_validate():
    dump(gnc)
    gnc2 = lcatr.schema.open("test_gnc.fits")
    gnc2.validate()
    dump(gnc2)

if __name__ == '__main__':
    test_empty()
    test_update()
    test_validate()
    test_write()
    test_read_and_validate()
