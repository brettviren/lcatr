#!/usr/bin/env python
'''
Test some things about a primary HDU
'''
from lcatr.base import *

def test_PrimaryHDU():
    print 'PrimaryHDU type: "%s"' % PrimaryHDU
    p = PrimaryHDU(name='TestResult')
    print 'PrimaryHDU instance type: "%s"' % type(p)

    try:
        p.validate()                # should not raise exception
    except ValueError, msg:
        print 'Failed to validate, but should have.'
        print msg
        print 'Header is:'
        print p.header
        raise
    print p.header


if __name__ == '__main__':
    test_PrimaryHDU()
