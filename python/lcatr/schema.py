#!/usr/bin/env python
'''
Wrap pyfits classes to support LCATR schema.

This wrapping adds the following methods to each HDU and HDUList classes

 - a validate()         raise an exception if the HDU is invalid

'''

from pyfits import *

def PrimaryHDU_validate(self):
    '''
    Validate a Primary HDU.
    '''
    self.verify()
    for name in ['EXTNAME','EXTVER']: self.header[name]
    return
PrimaryHDU.validate = PrimaryHDU_validate


def TableHDU_validate(self):
    '''
    Validate a TableHDU
    '''
    self.verify()
    for name in ['EXTNAME','EXTVER']: self.header[name]
    if not len(self.columns):
        raise ValueError,'TableHUD "%s" with no columns'%self.name
    return
TableHDU.validate = TableHDU_validate


def HDUList_validate(self):
    '''
    Validate a list of HDUs
    '''
    self.verify()
    for hdu in self:
        hdu.validate()
    return
HDUList.validate = HDUList_validate

def test_PrimaryHDU():
    p = pyfits.PrimaryHDU()
    try:
        p.validate()
    except KeyError,msg:
        print msg
        print 'as expected'
    else:
        raise RuntimeError,'validate did not fail on empty PrimaryHDU'

    p.update_ext_name('TestResult')
    p.update_ext_version(0)
    p.validate()                # should not raise exception
    print p.header

if __name__ == '__main__':
    test_PrimaryHDU()
