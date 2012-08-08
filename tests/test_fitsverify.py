#!/usr/bin/env python
'''
Test util.fitsverify
'''

import pyfits
from lcatr.util import fitsverify

good_file = 'test_fitsverify_good.fits'
bad_file = 'test_fitsverify_bad.fits'

def test_make_bad_file():
    columns = [pyfits.Column(name='BadColumn1', format='I', array=range(10), start=1),
               pyfits.Column(name='BadColumn2', format='I', array=range(10), start=2),]
    #print columns
    hdus = pyfits.HDUList([pyfits.PrimaryHDU(),
                           pyfits.new_table(columns, tbtype='BinTableHDU')])

    #print 'Writing "%s"' % bad_file
    hdus.writeto(bad_file, clobber=True)
    return

def test_make_good_file():
    hdus = pyfits.HDUList([pyfits.PrimaryHDU()])
    #print 'Writing "%s"' % good_file
    hdus.writeto(good_file, clobber=True)
    return
        

def _check(fname, expect_fail):
    res = fitsverify(fname)
    if res is None:
        success = True
    else:
        success = False

    if expect_fail and success:
        raise ValueError, 'Expected "%s" to fail, but it verified successfully' % fname

    if not expect_fail and not success:
        raise ValueError, 'Expected "%s" to succeed, but verification failed' % fname
        
    if expect_fail:
        msg = 'File %s failed as expected' % fname
    else:
        msg = 'File %s succeeded as expected' % fname
    print msg

def test_fitsverify_should_succeed():
    _check(good_file, False)

def test_fitsverify_should_fail():
    _check(bad_file, True)

if __name__ == '__main__':
    test_make_good_file()
    test_make_bad_file()
    test_fitsverify_should_fail()
    test_fitsverify_should_succeed()
