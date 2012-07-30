#!/usr/bin/env python
'''
Schema for the LIMS Metadata file
'''

import schema, util

class LimsMetaPrimaryHDU(schema.PrimaryHDU):
    '''
    Primary HDU for LIMS Metadata file.

    This HDU holds basic information about the test itself.

    To fill this HDU, each of the required cards should be given as
    keywords to the class or set after creation.
    '''

    canonical_name = 'LimsMeta'
    
    required_cards = [
        ('TESTNAME','Canonical name for the test result'),
        ('DATE-OBS','Time stamp of when test is run'),
        ('USERNAME','Name of operator/analyzer performing test'),
        ]

    def __init__(self, **kwds):
        super(LimsMetaPrimaryHDU,self).__init__()
        self.initialize_schema(**kwds)
        return

    pass




if __name__ == '__main__':
    import datetime, time

    meta = LimsMetaPrimaryHDU(testname = 'TestLimsMeta')
    meta.header.update('username','theycallmedog')
    try:
        meta.validate()
    except ValueError, msg:
        print msg
        print 'Got error on validation of partial primary HDU as expected'
        pass
    now = datetime.datetime(*time.gmtime()[:6])
    meta.header['date-obs'] = util.wash_card_value(now)
    print meta.header
    meta.validate()
