#!/usr/bin/env python
'''
Wrap pyfits classes to support LCATR schema.

This wrapping adds the following methods to each HDU and HDUList classes

 - a validate()         raise an exception if the HDU is invalid

'''

from pyfits import *

def validate_header_basics(header):
    for name in ['EXTNAME','EXTVER']: 
        header[name]            # just a reference to trigger an error
    return

def PrimaryHDU_validate(self):
    '''
    Validate a Primary HDU.
    '''
    self.verify()
    validate_header_basics(self.header)
    return
PrimaryHDU.validate = PrimaryHDU_validate

def TableHDU_validate(self):
    '''
    Validate a TableHDU
    '''
    self.verify()
    validate_header_basics(self.header)
    if not len(self.columns):
        raise ValueError,'TableHDU "%s": no columns' % self.name

    if not all([c.array for c in self.columns]):
        raise ValueError, 'TableHDU "%s": not all columns have arrays' % self.name

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
    p = PrimaryHDU()
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
