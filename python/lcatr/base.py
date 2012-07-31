#!/usr/bin/env python
'''
This module wraps pyfits classes to support LCATR schema.

This wrapping enhances and specializes the HDU pyfits classes.  To do
this it modifies the pyfits HDU classes and so must always be imported
first

  >>> import lcatr.base
  >>> import pyfits

It imports all of pyfits so strictly speaking one does not need to
import pyfits explicitly as on can reference all pyfits object via the
base module.  Or one can get familiar looking code via:

  >>> import lcatr.base as pyfits

To define specific schema, and provide validation code, inherit from
one of the HDU classes described below and provide their expected
extensions.

'''

import pyfits
import numpy
import util


# Some quantities and methods shared by all HDU classes.

#: All HDUs must supply these cards.
required_cards = [
    ('EXTNAME','Name of the HDU and its schema'),
    ('EXTVER' ,'Version of the HDU schema'),
    ]


class BaseHDU:
    '''
    Base HDU class.
    
    This base is multiply inherited by the HDU classes that replace
    the standard ``pyfits`` ones:

    * ``PrimaryHDU``
    * ``TableHDU``
    * ``BinTableHDU``

    to provide some additional methods.
    '''

    #: Specific HDU sub classes should set this to the list of required cards in the form:
    #:   >>> required_cards = [(name, comment), ...]
    required_cards = None

    #: Specify the name of the schema that this HDU follows.  
    schema_name = 'Generic'

    def required_card_desc(self):
        '''
        Return the list of required card descriptions
        '''
        mycards = self.required_cards or list()
        return required_cards + mycards

    def initialize_cards(self, **kwds):
        '''
        This method should be called by the constructor.

        Keyword arguments are interpreted as names of required cards
        (lower cased and with '-' replaced by '_') and are used to
        provided card values.  After construction cards may be set in the
        usual ``pyfits`` manner:

          >>> import datetime, time
          >>> from lcatr.base import PrimaryHDU
          >>> now = datetime.datetime(*time.gmtime()[:6])
          >>> hdu = PrimaryHDU(extname='TheSchema',date_obs=now)
          >>> hdu.header['extver'] = 0 # set schema version after construction
        '''
        self.update_ext_name(self.schema_name)
        self.update_ext_version(kwds.get('version',0))

        for name, comment in self.required_card_desc():
            if not self.header.has_key(name):
                self.header.update(name, '', comment)
                pass
            key = util.keywordify(name)
            val = kwds.get(key)
            if val is None: continue
            self.header[key] = val
            continue
        return

    def validate(self):
        '''
        Basic validation of an HDU.

        This will run pyfits verify() method and then check for required
        cards.

        ValueError is raise if validation fails.
        '''
        try:
            self.verify("exception")
        except VerifyError,msg:
            msg = 'HDU "%s/%s": verify failed: %s' % (self.schema_name, self.name, msg)
            raise ValueError,msg

        for name, comment in self.required_card_desc():
            value = self.header.get(name)
            if value is None:
                raise ValueError, '%s: required card: "%s" not set' % (self.schema_name,name)
            if value == '':
                raise ValueError, '%s: required card: "%s" is empty string' % (self.schema_name,name)
            print 'Header has required card: "%s" (%s)' % (name, comment)
            continue
        return
    pass

class PrimaryHDU(pyfits.PrimaryHDU, BaseHDU):
    '''
    Extension to pyfits.PrimaryHDU.
    
    The intial arguments to the constructor are the same as
    pyfits.PrimaryHDU.

      >>> hdu = PrimaryHDU(extname = 'TheSchemaName')
      >>> hdu.header['extver'] = 0 # the schema version

    see the BaseHDU.initialize_cards method for details.
    '''

    def __init__(self, data=None, header=None, do_not_scale_image_data=False, uint=False, **kwds):
        super(PrimaryHDU,self).__init__(data,header,do_not_scale_image_data,uint)
        self.initialize_cards(**kwds)
        return
    pass

class TableBaseHDU(BaseHDU):
    '''
    Base class for all Table HDUs.

Each subclass should define a .required_columns class data member which holds a li
    '''
    
    #: The list of descriptions of required columns in the form of a list of (name,type) doubles:
    #:  >>> required_columns = [('Col1Name','I'),...]
    required_columns = None

    # Internal, intialize the table base class.  Called by constructor.
    def initialize_table_base(self,**kwds):
        self.initialize_cards(**kwds)
        self.initialize_columns(**kwds)
        self.update_data()
        return

    def initialize_columns(self, **kwds):
        '''
        Intialized the required columns.  

        This method is called by the constructor and any kwds that
        match column names (first made lower case and '-' replaced by
        '_') will have their values treated as a column array.
        Otherwise the column will be created empty.
        '''
        if not self.required_columns: return
        cols = []
        for count,(name,typestr) in enumerate(self.required_columns):
            kwname = name.lower().replace('-','_')
            array = kwds.get(kwname,list())
            col = pyfits.Column(name=name, format=typestr, array=array, start=count+1)
            cols.append(col)
            continue
        self.columns = pyfits.ColDefs(cols)
        return

            

    def validate(self):
        '''
        Validate a table HDU
        '''
        #print '\nVALIDATING TableHDU "%s"\n-------------------' % self.name
        super(TableBaseHDU,self).validate()
        if not len(self.data):
            raise ValueError,'TableHDU "%s": no table data' % self.name
        return

    def get_column(self, column):
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

    def update_data(self, doppel = None):
        '''
        Update self.

        To stay consistent this must be called any time a column's array
        is modified directly.

        If another HDU is given its contents will be used instead of self's.
        '''
        # pyfits doesn't have a way to say "update my data" so we make a
        # temporary new table HDU and steal its guts as our own.
        if not doppel:
            doppel = new_table(self.columns, self.header)
        self.columns = doppel.columns
        self.header = doppel.header
        self.data = doppel.data
        return

    def set_column_array(self, column, array):
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
            pass
        col.array = array
        self.update_data()
        return

    def append_column_array(self, column, entry):
        '''
        Append entry to given column
        
        The column is specified either by its index (1-based) or name.
        
        This triggers update of the .data member.
        '''
        col = self.get_column(column)
        numpy.append(col.array, entry)
        self.update_data()
        return

    pass                        # TableBaseHDU

# note: need to do cut-and-paste programming here to retain the pyfits
# table HDU class dichotomy

class TableHDU(pyfits.TableHDU, TableBaseHDU):
    '''
    Extension to pyfits.TableHDU.
    '''
    def __init__(self, data=None, header=None, name=None, **kwds):
        super(TableHDU,self).__init__(data,header,name)
        kwds['extname'] = kwds.get('extname',name) # alias name->extname
        self.initialize_table_base(**kwds)
        return
    pass

class BinTableHDU(pyfits.BinTableHDU, TableBaseHDU):
    '''
    Extension to pyfits.BinTableHDU.
    '''
    def __init__(self, data=None, header=None, name=None, **kwds):
        super(BinTableHDU,self).__init__(data,header,name)
        kwds['extname'] = kwds.get('extname',name) # alias name->extname
        self.initialize_table_base(**kwds)
        return
    pass


pyfitsPrimaryHDU  = pyfits.PrimaryHDU
pyfitsTableHDU    = pyfits.TableHDU
pyfitsBinTableHDU = pyfits.BinTableHDU

pyfits.PrimaryHDU  = PrimaryHDU
pyfits.TableHDU    = TableHDU
pyfits.BinTableHDU = BinTableHDU



# This is just a simple bolt-on
def HDUList_validate(self):
    '''
    Validate a list of HDUs
    '''
    self.verify()
    for hdu in self:
        hdu.validate()
    return
pyfits.HDUList.validate = HDUList_validate


def hdu_pyfits2lcatr(hdu):
    '''
    Return an lcatr version of the plain pyfits HDU.
    '''
    import lcatr
    module = type(lcatr)

    for thing in dir(lcatr):
        if not isinstance(thing,module): 
            continue
        mod = lcatr.__dict__[thing]
        try:
            schema = mod.schema
        except AttributeError:
            continue
        if hdu.name != schema.name:
            continue

        # got a hit
        klass = schema.__class__
        new = klass()
        new.update_data(hdi)
        return new
    return None                 # go fish


def open(*args, **kwds):
    '''
    An LCATR-specific file reader.

    This will return lcatr versions.
    '''

    hl = pyfits.open(*args,**kwds)
    return pyfits.HDUList([hdu_pyfits2lcatr(hdu) for hdu in hl])
    

# import all of pyfits so users need not include pyfits 
from pyfits import *
