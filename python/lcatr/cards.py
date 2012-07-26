#!/usr/bin/env python
'''
Some specific cards
'''

from schema import Card

class ExtnameCard(Card):
    def __init__(self, value=None):
        base = super(ExtnameCard,self)
        base.__init__('EXTNAME','str','Canonical Name',
                      'Canonical name for the HDU', value)
        return
    pass

class SchemaVersionCard (Card):
    def __init__(self, value=0):
        base = super(SchemaVersionCard,self)
        base.__init__('SCHEMAV', 'int16', 'Schema Version',
                      'Version of schema used by this HDU', value)
        return
    pass

class TestNameCard(Card):
    def __init__(self, value=None):
        base = super(TestNameCard,self)
        base.__init__('TESTNAME', 'str', 'Canonical Test Name',
                      'Canonical test station name.', value)
        return
    pass

class TimeStampCard(Card):
    def __init__(self, value=None):
        base = super(TimeStampCard,self)
        base.__init__('DATE-OBS', 'datetime', 'Timestamp',
                      'A date and time stamp', value)
        return
    pass

class CommitHashCard(Card):
    def __init__(self, value=None):
        base = super(CommitHashCard,self)
        base.__init__('COMMIT',  'sha1', 'Commit hash',
                      'A GIT commit SHA1 digest hash.', value)
        return
    pass

class UsernameCard(Card):
    def __init__(self, username=None):
        base = super(UsernameCard,self)
        base.__init__('USERNAME', 'str', 'User name',
                      'The user name of the person operating the test station', 
                      username)
        return
    pass

if __name__ == '__main__':
    from hashlib import sha1
    chc = CommitHashCard()
    chc.set(sha1())
    print chc
    chc = CommitHashCard(sha1())
    print chc
