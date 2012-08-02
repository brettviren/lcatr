#!/usr/bin/env python
'''
'''

import pyfits
import sys
filename = sys.argv[1]

fp = pyfits.open(filename)
fp.info()
for hdu in fp:
    print
    print hdu.name
    print hdu.header
    print hdu.data
