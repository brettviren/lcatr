#!/usr/bin/env python
'''
Some specific cards
'''

from schema import Card

class ExtnameCard(Card):
    def __init__(self, value=None):
        super(ExtnameCard,self).__init__('EXTNAME','str','Canonical Name',
                                         'Canonical name for the HDU', value)
        return
    pass

class SchemaVersionCard (Card):
    def __init__(self, value=0):
        super(SchemaVersionCard,self).__init__('SchemaV', 'int16', 'Schema Version',
                                               'Version of schema used by this HDU', value)
        return
    pass

class TestNameCard(Card):
    def __init__(self, value=None):
        super(TestNameCard,self).__init__('TestName', 'str', 'Canonical Test Name',
                                          'Canonical test station name.', value)
        return
    pass

class TimeStampCard(Card):
    def __init__(self, value=None):
        super(TimeStampCard,self).__init__('DATE-OBS', 'datetime', 'Timestamp',
                                           'A date and time stamp', value)
        return
    pass

class CommitHashCard(Card):
    def __init__(self, value=None):
        super(CommitHashCard,self).__init__('Commit',  'sha1', 'Commit hash',
                                            'A GIT commit SHA1 digest hash.', value)
        return
    pass

if __name__ == '__main__':
    from hashlib import sha1
    chc = CommitHashCard()
    chc.set(sha1())
    print chc
    chc = CommitHashCard(sha1())
    print chc
