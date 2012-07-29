#!/usr/bin/env python
'''
Wrap pyfits classes to support LCATR schema.

This wrapping adds the following methods to each HDU and HDUList classes

 - validate()         raise an exception if the HDU is invalid

'''

from pyfits import *
import numpy

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
    #print '\nVALIDATING TableHDU "%s"\n-------------------' % self.name
    try:
        self.verify("exception")
    except VerifyError,msg:
        msg = 'TableHDU: "%s":' % self.name + str(msg)
        raise ValueError,msg
    validate_header_basics(self.header)

    if not len(self.data):
        raise ValueError,'TableHDU "%s": no table data' % self.name

    return
TableHDU.validate = TableHDU_validate
BinTableHDU.validate = TableHDU_validate

def TableHDU_get_column(self, column):
    '''
    Return column by name or (1-based) index.

    ValueError is raised if column not found.
    '''
    if isinstance(column,int):
        index = column - 1
    else:
        index = [c.name.lower() for c in self.columns].index(column.lower())
        pass

    try:
        col = self.columns[index]
    except IndexError:
        raise ValueError, 'TableHDU "%s": no column %s at index %s' % (column, index+1)
    return col
TableHDU.get_column = TableHDU_get_column
BinTableHDU.get_column = TableHDU_get_column

def TableHDU_update_data(self):
    '''
    Update the .data element.
    
    To stay consistent this must be called any time a column's array
    is modified directly.
    '''
    # pyfits doesn't have a way to say "update my data" so we make a
    # temporary new table HDU and steal its guts as our own.
    doppel = new_table(self.columns, self.header)
    self.columns = doppel.columns
    self.header = doppel.header
    self.data = doppel.data
    return
TableHDU.update_data = TableHDU_update_data
BinTableHDU.update_data = TableHDU_update_data

def TableHDU_set_column_array(self, column, array):
    '''
    Set a column's array.  

    The column is specified either by its index (1-based) or name.

    The array can be either a list or a numpy.array.

    ValueError is raised if column is not found.

    This triggers update of the .data member.
    '''
    col = self.get_column(column)
    if isinstance(array,list):
        array = numpy.array(array)
    col.array = array
    self.update_data()
    return
TableHDU.set_column_array = TableHDU_set_column_array
BinTableHDU.set_column_array = TableHDU_set_column_array

def TableHDU_append_column_array(self, column, entry):
    '''
    Append entry to given column

    The column is specified either by its index (1-based) or name.

    This triggers update of the .data member.
    '''
    col = self.get_column(column)
    numpy.append(col.array, entry)
    self.updagte_data()
    return


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
