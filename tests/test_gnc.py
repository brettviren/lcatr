#!/usr/bin/env python
'''
Test the GNC schema
'''

import lcatr
from hashlib import sha1

import test_gnc_data as tgd


def dump(gnc):
    gnc.info()
    for hdu in gnc:
        print hdu.header
        try:
            cols = hdu.columns
        except AttributeError:
            continue
        print cols
        for c in cols:
            print c.array
        print
        continue
    return

gnc = None

def test_empty():
    global gnc
    gnc = lcatr.gnc.GncResult()
    #dump(gnc)

def test_update():
    global gnc
    
    files = gnc['FileRefs'].columns
    files[0].array = tgd.analyzed_files
    files[1].array = [sha1().hexdigest() for x in tgd.analyzed_files]
    # fake the sha1 in this test since we don't have the actual result
    # files nor their sha1's around
    print gnc['FileRefs'].header
    print gnc['FileRefs'].columns
    #gnc['FileRefs'].update()
    for c in gnc['FileRefs'].columns:
        print c.array

    gains = gnc['Gains'].columns
    gains[0].array = tgd.linear_fit_gains
    gains[1].array = tgd.median_gains
    gnc['Gains'].update()
    
    noises = gnc['Noises'].columns
    noises[0].array = tgd.overscan_noise
    noises[1].array = tgd.stddev_noise
    gnc['Noises'].update()

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
    spots = gnc['ColdSpot'].columns
    spots[0].array = ampnum
    spots[1].array = pixcount
    spots[2].array = spotx
    spots[3].array = spoty
    gnc['ColdSpot'].update()

    #dump(gnc)

def test_validate():
    global gnc
    gnc.validate()

def test_write():
    '''
    Write to file 
    '''
    global gnc
    gnc.writeto("test_gnc.fits")

def test_read_and_validate():
    gnc2 = lcatr.schema.open("test_gnc.fits")
    gnc2.validate()

if __name__ == '__main__':
    test_empty()
    test_update()
    test_validate()
    test_write()
    test_read_and_validate()
