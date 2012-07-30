#!/usr/bin/env python

import datetime

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
