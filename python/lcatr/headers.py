#!/usr/bin/env python
'''
Some common header units
'''

import numpy as np
from schema import Header
from cards import *

class PrimaryHeader(Header):
    def __init__(self, test_name, user_name):
        cards = [ExtnameCard('Primary'), 
                 SchemaVersionCard(np.int16(0)), 
                 TestNameCard(test_name),
                 UsernameCard(user_name),
                 ]
        super(PrimaryHeader,self).__init__(cards)
        return
    pass

class MinimalHeader(Header):
    def __init__(self, name):
        cards = [ExtnameCard(name), SchemaVersionCard(np.int16(0))]
        super(MinimalHeader,self).__init__(cards)
        return
    pass

if __name__ == '__main__':
    ph = PrimaryHeader('ATestResult','theuser')
    print ph

    mh = MinimalHeader('AnHduWithMinimalHeader')
    print mh
