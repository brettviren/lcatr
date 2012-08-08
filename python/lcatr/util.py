#!/usr/bin/env python

import os
import datetime
import hashlib

def wash_datetime(dt):
    '''
    Return the given datetime in canonical form.  If not
    datetime.datetiem, return dt.
    '''
    if type(dt) != datetime.datetime: return dt
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

def wash_card_value(val):
    '''
    Convert a Python object to a form suitable for storing as a card value
    '''
    if isinstance(val,datetime.datetime): 
        return wash_datetime(val)
    return val

def keywordify(cardname):
    '''
    Convert a card name into a form suitable for use as a Python function keyword.
    '''
    return cardname.replace('-','_').lower()

def full_path(filename):
    '''
    Return the full path to a given filename or None if it is not found.
    
    Relative paths are searched under the current directory, then
    under a directory pointed to by a CCDTEST_ROOT environment
    variable (if defined) and finally by all directories listed in a
    $CCDTEST_PATH environment variable (if defined).
    '''
    if filename[0] == '/':
        if os.path.exists(filename): return filename
        return None

    paths = ['.'] \
        + os.environ.get('CCDTEST_ROOT',[]) \
        + os.environ.get('CCDTEST_PATH','').split(':')

    for dir in paths:
        check = os.path.join(dir,filename)
        if os.path.exists(check): return check
        continue
    return None

def sha1_digest(filename):
    '''
    Return a hashlib.sha1() object for the contents of the given file.
    The file is searched for via the full_path() function above.
    '''
    path = full_path(filename)
    if not path: return None
    return hashlib.sha1(open(path).read())


def fitsverify(filename):
    '''
    Run fitsverify on file of given name.  

    If verification fails, return list of error strings.

    The ``fitsverify`` program must be in the PATH.  It is obtained from:

    https://heasarc.gsfc.nasa.gov/docs/software/ftools/fitsverify/
    '''
    from subprocess import Popen, PIPE
    proc = Popen(['fitsverify',filename], stdout=PIPE, stderr=PIPE)
    out,err = proc.communicate()
    if not proc.returncode:
        return None

    ret = []
    for line in err.split('\n'):
        line = line.strip()
        if not line: continue
        ret.append(' '.join(line.split()[1:]))
        continue
    return ret

    
